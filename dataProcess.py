import yfinance as yf
import json
import pandas as pd

def fetch_ticker_data(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    return info, ticker

def extract_general_info(info):
    return {
        "company_name": info.get('longName', 'N/A'),
        "sector_industry": f"{info.get('sector', 'N/A')} / {info.get('industry', 'N/A')}",
        "description": info.get('longBusinessSummary', 'N/A'),
    }

def extract_financial_info(info):
    return {
        "Market Cap": info.get('marketCap', 'N/A'),
        "EBITDA": info.get('ebitda', 'N/A'),
        "PE Ratio": info.get('trailingPE', 'N/A'),
        "PEG Ratio": info.get('pegRatio', 'N/A'),
        "EPS": info.get('trailingEps', 'N/A'),
        "Book Value": info.get('bookValue', 'N/A'),
        "Dividend Share": info.get('dividendRate', 'N/A'),
        "Dividend Yield": info.get('dividendYield', 'N/A'),
        "Profit Margin": info.get('profitMargins', 'N/A'),
        "Operating Margin": info.get('operatingMargins', 'N/A'),
        "Return on Assets": info.get('returnOnAssets', 'N/A'),
        "Return on Equity": info.get('returnOnEquity', 'N/A'),
        "Revenue": info.get('totalRevenue', 'N/A'),
        "Revenue per Share": info.get('revenuePerShare', 'N/A'),
        # "Gross Profit": gross_profit,
        "Diluted EPS": info.get('trailingEps', 'N/A'),
        "Quarterly Earnings Growth": info.get('earningsQuarterlyGrowth', 'N/A')
    }

def extract_financial_statements(ticker):
    
    return {
        "income_statement": ticker.quarterly_financials.to_dict(orient="index"),
        "balance_sheet": ticker.quarterly_balance_sheet.to_dict(orient="index"),
        "cash_flow": ticker.quarterly_cashflow.to_dict(orient="index"),
    }

def process_tickers(ticker_symbols):
    results = {}
    for ticker_symbol in ticker_symbols:
        info, ticker = fetch_ticker_data(ticker_symbol)
        general_info = extract_general_info(info)
        financial_info = extract_financial_info(info)
        financial_statements = extract_financials(ticker)
        
        results[ticker_symbol.lower()] = {
            "general_info": general_info,
            "financial_info": financial_info,
            "financial_statements": financial_statements,
        }
    return results

def display_results(results):
    for ticker, data in results.items():
        print(f"\n{ticker} : {data['company_name']}")
        for key, value in data.items():
            if key in ['general_info', 'financial_info', 'financial_statements']:
                print(f"  {key}:")
                for sub_key, sub_value in value.items():
                    print(f"    {sub_key}: {sub_value}")
            else:
                print(f"  {key}: {value}")

def read_ticker_symbols_from_file(file_path):
    with open(file_path, 'r') as file:
        ticker_symbols = [line.strip() for line in file.readlines()]
    return ticker_symbols


def extract_financials(ticker):
    
    statements = {
        "income_statement": [], 
        "balance_sheet": [],
        "cash_flow": []
    }
    
    income_statement_df = ticker.quarterly_financials
    balance_sheet_df = ticker.quarterly_balance_sheet 
    cash_flow_df = ticker.quarterly_cashflow
    
    for df, statement_name in (
        (income_statement_df, "income_statement"),
        (balance_sheet_df, "balance_sheet"), 
        (cash_flow_df, "cash_flow")
    ):
        for date, row in df.T.iterrows():
            row = dict(row)
            row = {k: "NA" if pd.isna(v) else v for k, v in row.items()}
        
            quarter = f"Q{date.quarter} {date.year}"
            statements[statement_name].append({
                "date": date.isoformat(),
                "quarter": quarter,
                **row
            })
            
    return statements

def save_results_to_file(results, file_name):
    def convert(obj):
        if isinstance(obj, pd.Timestamp):
            return obj.strftime("%Y-%m-%d")
        return obj
    
    with open(file_name, 'w') as file:
        json.dump(results, file, default=convert, indent=4)

file_path = '/Users/margokim/Documents/hacklytics_topV/Top_100_Companies_Tickers.txt'
# Read ticker symbols from the file
ticker_symbols = read_ticker_symbols_from_file(file_path)

# Process the tickers
results = process_tickers(ticker_symbols)
file_name = '/Users/margokim/Documents/hacklytics_topV/ticker_data_results.json'
save_results_to_file(results, file_name)
