# importing library
from openai import OpenAI
import os


key = input("Enter your OpenAI API key: ")
client = OpenAI(api_key = key)

systemPersona = "You are an expert in finance and the technology industry."

company = "Apple"

userMessage = """As a financial analyst, you are tasked with conducting a comprehensive evaluation of a company's financial health and operational performance based on its latest financial data: the income statement, cash flow statement, and balance sheet. Please analyze the key metrics such as Gross Profit Margin, Operating Margin, Net Profit Margin, Current Ratio, Quick Ratio, Debt-to-Equity Ratio, and Free Cash Flow. Your analysis should cover the following aspects:

Profitability: Assess the company's ability to generate earnings as compared to its expenses and other relevant costs incurred during a specific period. Calculate and interpret the various profit margins and discuss the trends observed over recent periods.

Liquidity: Evaluate the company's capacity to pay off its short-term liabilities with its short-term assets. Provide insights into the Current and Quick Ratios and what they indicate about the company's financial health.

Operational Efficiency: Examine how efficiently the company uses its assets to generate income and cash. Look into cash flow metrics and turnover ratios, and explain their implications for the company's operational success.

Financial Stability: Investigate the company's long-term financial health, focusing on its use of debt versus equity financing. Analyze the Debt-to-Equity Ratio and changes in working capital, and discuss their significance.

Conclude your analysis by summarizing the company's overall financial condition, highlighting its strengths and weaknesses. Your evaluation will assist investors and company management in understanding the fundamentals of the company and making informed decisions.

The company that you will be analyzing is {company}.
The following will be the data that you can use. 

Please do not use other data sources.

Please limit your response to no more than 200 words."""

completion = client.chat.completions.create(
  model="gpt-4-0613",
  messages=[
    {"role": "system", "content": systemPersona},
    {"role": "user", "content": userMessage}
  ]
)

print(completion.choices[0].message.content)
