import streamlit as st
import pandas as pd

from langchain_ollama import OllamaLLM
from langchain_experimental.agents import create_pandas_dataframe_agent

st.title('AI Assistant for Data Science')
st.header('Exploratory Data Analysis Part')
st.subheader('Solution')
st.write('Hello, I am AI Assistant and I am here to help you with data science projects')
