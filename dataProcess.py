import yfinance as yf

def fetch_ticker_data(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    return info

# def extract_general_info(info):
#     return {
#         "Company Code and Name": f"{info.get('symbol', 'N/A')} - {info.get('longName', 'N/A')}",
#         "Sector/Industry": f"{info.get('sector', 'N/A')} / {info.get('industry', 'N/A')}",
#         "Company Description": info.get('longBusinessSummary', 'N/A'),
#     }


def extract_general_info(info):
    # Assuming EBITDA as a proxy for gross profit; might need adjustment based on actual data structure
    gross_profit = info.get('ebitda', 'N/A')
    
    return {
        "Company Code and Name": f"{info.get('symbol', 'N/A')} - {info.get('longName', 'N/A')}",
        "Sector/Industry": f"{info.get('sector', 'N/A')} / {info.get('industry', 'N/A')}",
        "Company Description": info.get('longBusinessSummary', 'N/A'),
    }


def extract_financial_info(info):
    # gross_profit = info.get('ebitda', 'N/A')
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
        "Quarterly Earnings Growth": info.get('earningsQuarterlyGrowth', 'N/A'),
        # Add more fields as needed
    }

def extract_technical_indicators(info):
    return {
        "Beta": info.get('beta', 'N/A'),
        "52 Week High/Low": f"{info.get('fiftyTwoWeekHigh', 'N/A')} / {info.get('fiftyTwoWeekLow', 'N/A')}",
        # Add more fields as needed
    }

def process_tickers(ticker_symbols):
    results = {}
    for ticker_symbol in ticker_symbols:
        ticker = yf.Ticker(ticker_symbol)
        info = fetch_ticker_data(ticker_symbol)
        general_info = extract_general_info(info)
        financial_info = extract_financial_info(info)
        technical_indicators = extract_technical_indicators(info)
        financial_statements = extract_financial_statements(ticker)
        
        # Combine all extracted information
        results[ticker_symbol] = {
            "General Info": general_info,
            "Financial Info": financial_info,
            "Technical Indicators": technical_indicators,
            "Financial Statements": financial_statements
        }
    return results


def extract_financial_statements(ticker):
    # Fetches quarterly financial statements
    quarterly_financials = ticker.quarterly_financials
    quarterly_balance_sheet = ticker.quarterly_balance_sheet
    quarterly_cashflow = ticker.quarterly_cashflow

    return {
        "Quarterly Financials": quarterly_financials,
        "Quarterly Balance Sheet": quarterly_balance_sheet,
        "Quarterly Cash Flow": quarterly_cashflow,
    }



def display_results(results):
    for ticker_symbol, data in results.items():
        print(f"\nTicker: {ticker_symbol}")
        for category, info in data.items():
            print(f"\n{category}:")
            for key, value in info.items():
                print(f"  {key}: {value}")





# Example S&P 100 tickers - Replace with the full list of S&P 100 tickers
ticker_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN"]

# Process the tickers
results = process_tickers(ticker_symbols)

# Display the results
display_results(results)
