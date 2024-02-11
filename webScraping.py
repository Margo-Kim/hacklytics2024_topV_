from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json

def get_data_for_ticker(ticker):
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Uncomment to run browser in background
    driver = webdriver.Chrome(service=service, options=options)

    url = f'https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}'
    driver.get(url)
    time.sleep(10)  # Adjust based on your internet speed

    page_source = driver.page_source
    driver.quit()

    soup = BeautifulSoup(page_source, 'html.parser')
    tables = soup.find_all('table')

    # Initialize dictionaries for quarterly data and other data
    quarterly_data = {}
    other_data = {}

    # Process only the first table for quarterly data
    first_table_rows = tables[0].find_all('tr')
    headers = first_table_rows[0].find_all('th')
    header_texts = [header.text.strip() for header in headers]  # Extract header texts

    for row in first_table_rows[1:]:  # Skip header row
        cols = row.find_all('td')
        metric_name = cols[0].text.strip()
        for i, col in enumerate(cols[1:], start=1):  # Skip metric name column
            date = header_texts[i]
            value = col.text.strip()
            if date not in quarterly_data:
                quarterly_data[date] = {}
            quarterly_data[date][metric_name] = value

    # Combine specified tables (2, 6, and 7) for other data
    for table_number, table in enumerate(tables[1:], start=2):  # Skip the first table
        if table_number in [2, 6, 7]:  # Only process tables 2, 6, and 7
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all(['th', 'td'])
                if len(cols) == 2:  # Key-value pairs
                    metric_name, value = cols[0].text.strip(), cols[1].text.strip()
                    other_data[metric_name] = value

    # Format the data according to the specified structure
    ticker_data = {
        "Quarterly Data": quarterly_data,
        "Other Data": other_data
    }

    return ticker_data

def read_ticker_symbols_from_file(file_path):
    with open(file_path, 'r') as file:
        ticker_symbols = [line.strip() for line in file.readlines()]
    return ticker_symbols


def save_results_to_file(results, file_name):
    with open(file_name, 'w') as file:
        json.dump(results, file, indent=4)

# file_path = '/Users/margokim/Documents/hacklytics_topV/Top_100_Companies_Tickers.txt'
# # Read ticker symbols from the file
# ticker_symbols = read_ticker_symbols_from_file(file_path)

ticker_symbols = ["T", "ABBV", "ABT", "ACN", "ADBE", "AMD", "GOOGL", "GOOG"]



all_tickers_data = {}

for ticker in ticker_symbols:
    all_tickers_data[ticker] = get_data_for_ticker(ticker)

file_name = '/Users/margokim/Documents/hacklytics_topV/price_dynamics_results.json'
save_results_to_file(all_tickers_data, file_name)
