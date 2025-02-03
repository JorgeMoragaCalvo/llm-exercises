import streamlit as st
import pandas as pd

from langchain_ollama import OllamaLLM
from langchain_experimental.agents import create_pandas_dataframe_agent

st.title('AI Assistant for Data Science')
st.header('Exploratory Data Analysis Part')
st.subheader('Solution')
st.write('''Hello, I'm AI Assistant and I'm here to help you with data science projects''')

with st.sidebar:
    st.write('*Your Data Science adventure begins with a CSV file.*')
    st.caption('**You may already know that every exciting data science journey starts with a dataset**')

    st.divider()

    st.caption("<p style = 'text-align:center'>Made By Me</p>", unsafe_allow_html=True)