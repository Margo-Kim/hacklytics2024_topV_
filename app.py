import streamlit as st
import streamlit_authenticator as stauth
import os
from pymongo import MongoClient
import pymongo
from langchain.chat_models import ChatOpenAI
from aggreate import *

#MONGO_URI = os.getenv("MONGO_URI")
MONGO_URI="mongodb+srv://minwoos803:test123@cluster0.9h4mtcf.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client.finance
macro = db.macro
company = db.company2

running = True

if running:
    alphaPulseLogo = "updatedLogo.png"
    st.image(alphaPulseLogo, caption=None, width=200, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

    # Sidebar for navigation
    page = st.sidebar.radio("Choose a page", ["Home", "Stock Selection"])

    if page == "Home":
        st.title("Welcome to AlphaPulse!")
        st.header("You are one click away from knowledge.")
        st.write("AlphaPulse is an innovative platform that provides a comprehensive suite of financial and market data, analysis, and insights to help you make informed investment decisions. Our platform leverages cutting-edge AI technologies to deliver real-time, actionable intelligence that empowers you to stay ahead of the market and maximize your investment returns.")

    elif page == "Stock Selection":
        
        if 'api_key' not in st.session_state:
            st.session_state.api_key = ""


        apiKey = st.text_input("Please enter your API key", type="password")
        st.session_state.api_key = apiKey


        ticker = st.text_input("Please enter the ticker below.", placeholder="eg: AAPL").lower()
         
        if st.session_state.api_key:
                os.environ["OPENAI_API_KEY"] = st.session_state.api_key     

        if st.button("Submit"):
            if st.session_state.api_key:
                company_description = getCompanyDescription(ticker)
                st.write(company_description)

                customResponse = generate_custom_response(ticker, st.session_state.api_key)
                st.write(customResponse)
            else:
                st.warning("Please enter your API key.")


