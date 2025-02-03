import streamlit as st
import pandas as pd

from langchain_ollama import OllamaLLM
from langchain_experimental.agents import create_pandas_dataframe_agent

st.title('AI Assistant for Data Science 🤖')
st.write('''Hello :hand:, I'm AI Assistant and I'm here to help you with data science projects''')

with st.sidebar:
    st.write('*Your Data Science adventure begins with a CSV file.*')
    st.caption('**You may already know that every exciting data science journey starts with a dataset**')

    with st.expander('an expander'):
        st.write('Expander text')

    st.divider()

    st.caption("<p style = 'text-align:center'>Made By Me</p>", unsafe_allow_html=True)

if st.button("Let's get started"):
    st.header('Exploratory Data Analysis Part')
    st.subheader('Solution')
    
user_csv = st.file_uploader("Upload your file here", type="csv")
