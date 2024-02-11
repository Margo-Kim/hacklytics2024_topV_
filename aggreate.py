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



#MONGO_URI = os.getenv("MONGO_URI")
MONGO_URI="mongodb+srv://minwoos803:test123@cluster0.9h4mtcf.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client.finance
macro = db.macro
company = db.company2
summary = db.summary
neighbor = db.neighbor


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
ticker = 'aapl'
company_data = fetch_company_data(ticker)
print(company_data)



# openai_api_key = getpass()
# os.environ["OPENAI_API_KEY"] = openai_api_key
# openai.api_key = openai_api_key

chat = ChatOpenAI(temperature=0.0, model_name='gpt-4-turbo-preview')

template_string = """
As an AI expert in finance and the technology industry, you are provided with a comprehensive set of data summaries reflecting a company’s performance over the past month. \n
This data encompasses news article summaries, analyses of stock price dynamics, fundamental financial metrics, and the impact of macroeconomic factors. \n
Your task is to synthesize this information to offer a reasoned perspective on the company’s future outlook.

All the information about compnay is provided in : {compnay_info}

Based on this data, provide a concise summary (approximately 100 words) that integrates these insights to conclude whether the outlook for company is bullish or bearish for the upcoming month. \n
Consider the company’s ability to navigate challenges, capitalize on opportunities, and its overall financial health in your analysis. Your summary should help investors and company management understand the fundamental stance on the company and guide informed decision-making.

"""
prompt_template = ChatPromptTemplate.from_template(template_string)
prompt_template.messages[0].prompt.input_variables

def generate_outlook(compnay):
    test_input1 = prompt_template.format_messages(
                      compnay_info = compnay
    )

    response = chat(test_input1)
    return response.content


# Example usage
outlook = generate_outlook(company_data)
print(outlook)
