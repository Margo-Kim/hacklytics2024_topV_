import os
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
#from langchain_openai import ChatOpenAI
from getpass import getpass
import openai
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
from pymongo import MongoClient
import pymongo

from langchain.prompts import PromptTemplate, HumanMessagePromptTemplate
from langchain.schema import HumanMessage
from langchain.embeddings.openai import OpenAIEmbeddings
from openai import OpenAI



#MONGO_URI = os.getenv("MONGO_URI")
MONGO_URI="mongodb+srv://minwoos803:test123@cluster0.9h4mtcf.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client.finance
macro = db.macro
company = db.company2
summary = db.summary
neighbor = db.neighbor
dynamic = db.dynamic
structured = db.structured    


def fetch_company_data(ticker):
    #collections = ['financial_market_data', 'company_general_info', 'inter_company_relationships']
    collections = ['company2', 'macro', 'summary', 'neighbor']
    company_data = {}

    for collection_name in collections:
        collection = db[collection_name]
        document = collection.find_one({"ticker": ticker})

        if document:
            # Assuming you want to remove the MongoDB specific '_id' field
            document.pop('_id', None)
            company_data[collection_name] = document

    return company_data

# Example usage
# ticker = 'aapl'
# company_data = fetch_company_data(ticker)
# print(company_data)

def queryVariable(ticker):
    document = company.find_one({"ticker": ticker}, {"_id": 0, "general_info": 1})
    company_name = document['general_info']['company_name']
    sector_industry = document['general_info']['sector_industry']
    description = document['general_info']['description']

    document1 = summary.find_one({"ticker": ticker})
    if document1 and 'reports' in document1:
        progressiveNews = document1['reports']
    else:
        progressiveNews = "No news available for the company."

    document2 = structured.find_one({"ticker": ticker})
    if document2 and "details" in document2:
        fundamentalData = document2['details']
    else:
        fundamentalData = "No fundamental data  available for the company."

    document3 = dynamic.find_one({"ticker": ticker})
    if document3 and "summary" in document3:
        priceDynamic = document3['summary']
    else:
        priceDynamic = "No price dynamic available for the company."

    query = {"reportTitle": "Summary of the 2023 US Economic Outlook by Goldman Sachs"}
    # Execute the query and extract the 'categories' field
    document4 = macro.find_one(query, {'categories': 1, '_id': 0})
    if document4 and 'categories' in document4:
        macroData = document4['categories']
    else:
        macroData = "No macrodata available."
    
    return company_name, description, progressiveNews, fundamentalData, priceDynamic, macroData
    
    # print(progressiveNews)
    # print('==========')
    # print(fundamentalData)
    # print('==========')
    # print(priceDynamic)
    # print('==========')
    # print(macroData)


# openai_api_key = getpass()
# os.environ["OPENAI_API_KEY"] = openai_api_key
# openai.api_key = openai_api_key

DEAFULT_PROMPT_TEMPLATE_TEXT = """
In the ever-evolving landscape of the stock market, making informed investment decisions requires a deep dive into a myriad of factors that can influence stock performance. This necessitates a comprehensive analysis that spans company-specific news, fundamental performance metrics, stock price trends, and overarching economic conditions. I am in pursuit of an analysis that meticulously examines these elements to forecast the future direction of the company {company}, offering insights into their short, mid, and long-term potential.\n
You have four categories of data to consider in your analysis: \n
Progressive News Data: Monthly summaries of the company's news, highlighting significant events, product launches, partnerships, or any controversies that could impact investor perception. \n
Here is the news for the company. 
\n{progressiveNews}\n
Company Fundamental Data: Quarterly updates on company performance, including earnings reports, revenue growth, expense trends, and profitability metrics. This category provides a snapshot of the company's financial health and operational efficiency.\n
Here is the company fundamental data. 
\n{fundamentalData}\n
Stock Price Dynamics: An analysis of stock price movements, trading volumes, and volatility. This includes an examination of technical indicators, historical price trends, and any patterns that could suggest future movements.\n
Here is the stock price dynamics. 
\n{priceDynamic}\n
Macroeconomic Indicators: General economic trends that could influence the stock market at large, including interest rates, inflation data, employment figures, and GDP growth rates. These indicators help contextualize the company's performance within the broader economic landscape. \n
Here is the macroeconomic data. 
\n{macroeconomic}\n
Your taks is to leverage the provided data to predict the stock performance of selected companies or sectors over short (1-3 months), mid (4-12 months), and long-term (1-5 years) horizons. Each prediction should be classified as either bearish or bullish, based on a thorough analysis of the aforementioned data categories. \n
Here are some suggesions on how to approach this: \n
Short-Term Outlook: Utilize progressive news data and recent stock price dynamics to gauge immediate market sentiment and potential short-term movements. \n
Mid-Term Outlook: Incorporate company fundamental data and any anticipated macroeconomic changes to assess the stock's mid-term trajectory, considering upcoming financial reports or sector trends. \n
Long-Term Outlook: Analyze long-term economic forecasts alongside the company's strategic initiatives as reported in fundamental data and news summaries to predict the stock's long-term performance. \n
Here are some guiding principles when it comes to your work. Ensure your analysis is grounded in the provided data, drawing clear connections between data insights and your predictions. Maintain transparency regarding the analytical methods and assumptions used throughout the process. Present a balanced perspective that considers both potential growth opportunities and risks. \n
Here are some recommendations for your writing style. Aim for clarity and conciseness, making complex information accessible and understandable. Use direct language to articulate your predictions and the rationale behind them. \n
Please note, when providing your response, start directly with your prediction on whether the short term, mid term, and long term outlook is bullish or bearish. Then, provide a brief summary of the rationale behind your prediction. \n
By meticulously analyzing these diverse data sets, your comprehensive outlook will serve as a valuable resource for the investment community, guiding them towards informed decision-making in an uncertain market environment."""


PROMPT_TEMPLATE = PromptTemplate(
template=DEAFULT_PROMPT_TEMPLATE_TEXT,
input_variables=["company", "progressiveNews", "fundamentalData", "priceDynamic", "macroeconomic"])

def getModelResponse(apiKey, prompt):
    client = OpenAI(api_key = apiKey)
    completion = client.chat.completions.create(model = "gpt-4-0125-preview",
                                                messages=[ {"role": "user", "content": prompt}])
    return completion.choices[0].message.content

    # response = openai.completions.create(model = mdl, prompt=input_prompt)
    # return response.choices[0].text.strip()

    # messages = [HumanMessage(content=input_prompt)]

    # return mdl(messages)


#| export
def generate_custom_prompt(ticker):

    company_name, description, progressiveNews, fundamentalData, priceDynamic, macroData = queryVariable(ticker)

    company = company_name # company data
    progressiveNews = progressiveNews # progressive news data
    fundamentalData = fundamentalData # fundamental data
    priceDynamic = priceDynamic # stock price dynamics
    macroeconomic = macroData # macroeconomic data

    # Fill the prompt
    filled_prompt = PROMPT_TEMPLATE.format(company=company, progressiveNews=progressiveNews, fundamentalData=fundamentalData, priceDynamic=priceDynamic, macroeconomic=macroeconomic)

    return filled_prompt

#| export
def generate_custom_response(ticker, apiKey):
    # create customized prompts
    customized_prompt = generate_custom_prompt(ticker)
    print(customized_prompt)

    # get response
    draft_response = getModelResponse(apiKey, customized_prompt)

    return draft_response

def getCompanyDescription(ticker):
    document = company.find_one({"ticker": ticker}, {"_id": 0, "general_info": 1})
    description = document['general_info']['description']
    return description



# prompt_template = ChatPromptTemplate.from_template(performanceTemplate)
# prompt_template.messages[0].prompt.input_variables
# 
# def generateCustomTemplate(ticker):
#     company_info = "AAPL"
#     return performanceTemplate
# 
# def generateCustomResponse(ticker, company_data):
#     return ticker

# Example usage
# outlook = generate_outlook(company_data)
# print(outlook)

# os.environ["OPENAI_API_KEY"] = input("Enter your OpenAI API key: ")
# chatModel = ChatOpenAI(model_name='gpt-4-0125-preview', temperature=0.1)
# print(generate_custom_response("AAPL", chatModel))