import streamlit as st
import streamlit_authenticator as stauth
import os
from pymongo import MongoClient
import pymongo

#MONGO_URI = os.getenv("MONGO_URI")
MONGO_URI="mongodb+srv://minwoos803:test123@cluster0.9h4mtcf.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client.finance
macro = db.macro
company = db.company2

running = True

if running:

    # Sidebar for navigation
    page = st.sidebar.radio("Choose a page", ["Main", "Stock Selection"])

    if page == "Main":
        st.title("Welcome!")
        st.write("This is the main page of our Financial AI. At here, simply enter your ticker, and with a single click of a button, you can get the latest market performance expectation of your desired company.")

    elif page == "Stock Selection":
        st.title("Please enter the stock ticker below.")

        ticker = st.text_input("Please enter the ticker below.", placeholder="eg: AAPL").lower()
        if ticker:
            if st.button("Submit"):
                # Query MongoDB for the document with the matching company_code
                document = company.find_one({"company_code": ticker}, {"_id": 0, "general_info": 1})
                
                if document and "general_info" in document:
                    st.write("You have entered the ticker of:", ticker.upper())
                    st.write("General Information:")
                    for key, value in document["general_info"].items():
                        st.text(f"{key}: {value}")
                else:
                    st.write("No information found for ticker:", ticker.upper())