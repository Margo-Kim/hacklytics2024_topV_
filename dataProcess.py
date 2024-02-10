import yfinance as yf

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
    # Simplify the financial statements for demonstration
    # This is a placeholder; the actual implementation would depend on how you want to format the financial statements.
    return {
        "income_statement": ticker.quarterly_financials.to_dict(),
        "balance_sheet": ticker.quarterly_balance_sheet.to_dict(),
        "cash_flow": ticker.quarterly_cashflow.to_dict(),
    }

def process_tickers(ticker_symbols):
    results = {}
    for ticker_symbol in ticker_symbols:
        info, ticker = fetch_ticker_data(ticker_symbol)
        general_info = extract_general_info(info)
        financial_info = extract_financial_info(info)
        financial_statements = extract_financial_statements(ticker)
        
        results[ticker_symbol.lower()] = {
            "ticker": ticker_symbol.lower(),
            "company_name": general_info['company_name'],
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

# Example S&P 100 tickers - Replace with the full list of S&P 100 tickers
ticker_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN"]
ticker_symbols = ["AAPL"]

# Process the tickers
results = process_tickers(ticker_symbols)

# Display the results
print(results)
