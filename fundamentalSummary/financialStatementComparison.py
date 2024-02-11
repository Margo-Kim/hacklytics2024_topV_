import json

def extract_financial_data(financial_statements, statement_type, quarter_pairs):
    extracted_data = {}
    statements = financial_statements.get(statement_type, [])
    
    for quarter_pair in quarter_pairs:
        comparison_key = f"{quarter_pair[0]} vs {quarter_pair[1]}"
        extracted_data[comparison_key] = {
            statement_type: {}
        }
        for quarter in quarter_pair:
            for statement in statements:
                if statement['quarter'] == quarter:
                    for key, value in statement.items():
                        if key not in ['date', 'quarter']:  # Exclude date and quarter from metrics
                            if key not in extracted_data[comparison_key][statement_type]:
                                extracted_data[comparison_key][statement_type][key] = {}
                            extracted_data[comparison_key][statement_type][key][quarter] = value
    return extracted_data

# Load JSON data for all tickers
all_tickers_data = {}  # Assuming all_tickers_data is already loaded as shown previously
# Example: Load your JSON file here if not loaded previously
file_path = '/content/ticker_data_results.json'  # Update this path to your JSON file location

with open(file_path, 'r') as json_file:
    all_tickers_data = json.load(json_file)

quarters_to_compare = [['Q1 2023', 'Q2 2023'], ['Q2 2023', 'Q3 2023'], ['Q3 2023', 'Q4 2023']]
all_tickers_processed_data = {}

for ticker, data in all_tickers_data.items():
    all_comparison_data = {}
    for statement_type in ['income_statement', 'balance_sheet', 'cash_flow']:
        all_comparison_data[statement_type] = extract_financial_data(data['financial_statements'], statement_type, quarters_to_compare)

    all_tickers_processed_data[ticker] = all_comparison_data

# Save the processed data to a JSON file
file_name = 'merged_financial_data.json'
with open(file_name, 'w') as json_file:
    json.dump(all_tickers_processed_data, json_file, indent=4)

print(f"All tickers' financial data has been merged and saved in {file_name}.")
