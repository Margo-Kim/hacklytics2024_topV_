#  AlphaPulse
![Logo](updatedLogo.png)
## Hacklytics 2024 Finance & Gen AI Track
## Short, Mid, Long Terms Stock Performance Prediction System
The intersection of media news and stock price has long been studied. https://www.tcd.ie/Economics/assets/pdf/SER/2019/11stock_prices.pdf.
Yet, stock price is not the only indicator that look for when engaging with the stock market.
The intricacy of the stock market, coupled with the necessity for high financial literacy and extensive experience, often deters individuals from participating and limits small to mid-sized companies in managing complex portfolios with constrained resources.

AlphaPulse is an innovative AI-driven framework designed to transform unstructured financial data into actionable investment insights. By leveraging the power of LLM, AlphaPulse offers an in-context-learning approach to stock performance analysis, providing users with sophisticated stock performance outlook backed by detailed explanations.

## Methodology

AlphaPulse combines GPT-4's natural language processing and generative AI capabilities with advanced financial analysis techniques. It synthesizes information from diverse sources to generate investment signals, emulating professional investment teams' decision-making processes. Key components include:

- **Daily News Summary:** Monthly narratives by company from daily news.
- **Fundamentals Summary:** Comparative analysis of financial statements.
- **Stock Price Dynamics Summary:** Evaluation of stock performance against the market and peers.
- **Macroeconomic Summary:** Overview of the economic climate.
- **Outlook & Reasoning:** Expert recommendations with detailed rationale.

## Data Sources

AlphaPulse utilizes data from various sources to analyze and provide investment insights:

- **Stock Price Data** from Yahoo Finance for S&P 100 stocks.
- **Financial News** via Perigon API, with over 68,000 daily news entries.
- **Company Fundamentals** web scraped from Yahoo Finance.
- **Macroeconomic Reports** from notable economic outlooks like Goldman Sachs's 2023 report.

## Development Process

1. **Data Collection Pipeline:** Gathering relevant data using the Perigon API and web scraping from Yahoo Finance.
2. **Data Summarization:** Employing GPT-4 with custom prompt engineering for summarizing data, also supported by the text-embedding-ada-002 model for comparative analysis.
3. **Data Storage:** Using MongoDB Atlas as a NoSQL database for unstructured data management.
4. **User Interface Development:** Creating an interactive UI with Streamlit for user interaction and signal generation.

## Output Predictions
AlphaPulse's user interface delivers predictions in three distinct timeframes:

- **Short-Term Prediction:** Offers an immediate outlook on the stock's performance, indicating whether a bullish or bearish trend is expected in the short term (1-4 months).
- **Mid-Term Prediction:** Provides insight into the stock's trajectory over the medium term, helping users understand potential bullish or bearish movements (4-12 months).
- **Long-Term Prediction:** Projects the long-term trend of the stock, offering a broader perspective on its bullish or bearish potential (1-5 years).

These predictions are generated based on a comprehensive analysis of current market dynamics, financial news, company fundamentals, and macroeconomic factors, ensuring users receive well-informed recommendations for their investment strategies.

Disclaimer: AlphaPulse's AI-driven stock performance outlooks and recommendations are intended for informational purposes only and should not be considered financial advice, with users responsible for their own investment decisions and understanding that past performance is not indicative of future results.


## Getting Started

To explore AlphaPulse, clone this repository and follow the setup instructions in our documentation to get the system running on your local machine. Ensure you have access to the necessary APIs and MongoDB Atlas for data storage and retrieval.

## Contribution
Team: TopV 
- Jasmine G.
- Minwoo S.
- Margo K.
- Qi L.



