import json
import openai
import re

def read_json(file_path):
    """Reads JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def format_quarter_comparisons(data):
    """Formats the quarter comparison data for inclusion in the prompt."""
    formatted_data = ""
    for comparison, details in data.items():
        formatted_data += f"\n\n### {comparison} Comparison:"
        for statement_type, metrics in details.items():
            formatted_data += f"\n- **{statement_type.replace('_', ' ').capitalize()}**:"
            for metric, values in metrics.items():
                changes = ", ".join([f"{quarter}: {value}" for quarter, value in sorted(values.items())])
                formatted_data += f"\n  - {metric}: {changes}"
    return formatted_data.strip()



import re

def parse_summary_to_dict(summary):
    """Parses the summary into a dictionary based on main categories."""
    categories = ["Profitability", "Revenue Growth", "Debt Levels", "Cash Flow", "Assets and Equity", "Conclusion"]
    summary_dict = {}
    for category in categories:
        # This pattern accounts for varying markdown levels and captures the content up to the next heading or end of text
        pattern = rf"#+\s*{category}\s*[^#]+"
        match = re.search(pattern, summary, re.IGNORECASE | re.DOTALL)
        if match:
            # Extract the text after the category name
            content = match.group(0)
            # Remove the category name and any leading/trailing whitespace
            content = re.sub(rf"^#+\s*{category}\s*", '', content, flags=re.IGNORECASE).strip()
            # Replace newline characters with commas if necessary for your structure
            content = content.replace('\n', ', ')
            summary_dict[category] = content
        else:
            summary_dict[category] = "Not available"
    return summary_dict


def save_to_json(data, filename):
    """Saves the data to a JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def generate_summary(company, quarter_comparisons_formatted):
    """Generates a financial summary based on the formatted quarter comparisons."""
    system_persona = "You are an expert in finance and the technology industry."
    user_message = f"""
    {system_persona}
    
    Create a comprehensive financial summary for {company.upper()}, analyst writing format changes in three consecutive quarter comparisons in sentences.{quarter_comparisons_formatted}
    KEEP THE CATEGORIES AND DO NOT CHANGE THE CATEGORY NAMES. CATEGORIES = ["Profitability", "Revenue Growth", "Debt Levels", "Cash Flow", "Assets and Equity", "Conclusion"]
    - Profitability: Highlight the changes in net income and gross profit, reflecting on the company's profitability.
    - Revenue Growth: Discuss the changes in total revenue, indicating the company's growth or contraction in market share and sales.
    - Debt Levels: Analyze total liabilities, long-term debt, short-term debt, and net debt, providing insights into the company's financial leverage and stability.
    - Cash Flow: Examine net cash from operating activities, capital expenditure, and end cash position to assess liquidity and operational efficiency.
    - Assets and Equity: Review total assets and stockholder equity to comment on the company's asset management and valuation.
    - Conclusion: Your overall conclusion of the company performance based on the financial input. 
    """
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You are a highly knowledgeable financial analyst."},
            {"role": "user", "content": user_message}
        ]
    )
    
    return response.choices[0].message['content']

# Main code execution
if __name__ == "__main__":
    key = input("Enter your OpenAI API key: ")
    openai.api_key = key
    ticker_symbols = ["AAPL", "T", "ABBV", "ABT", "ACN", "ADBE", "AMD", "GOOGL", "GOOG"]

    #ticker_symbols = ["AAPL", "ABBV", "ABT" ]  # Example ticker symbols
    json_file_path = '/content/merged_financial_data.json'
    json_data = read_json(json_file_path)

    summaries = {}
    for company in ticker_symbols:
        quarter_comparisons = format_quarter_comparisons(json_data[company.lower()])  
        summary = generate_summary(company, quarter_comparisons)
        print(summary) 
        structured_summary = parse_summary_to_dict(summary)
        summaries[company] = structured_summary
    

    # Save the structured summaries to a JSON file
    save_to_json(summaries, 'structured_financial_summaries.json')

    print("Summaries have been generated and saved to 'structured_financial_summaries.json'.")
