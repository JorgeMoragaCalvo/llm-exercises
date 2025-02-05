import streamlit as st
import pandas as pd

from langchain_ollama import OllamaLLM
from langchain_experimental.agents import create_pandas_dataframe_agent

llm = OllamaLLM(model="deepseek-r1:1.5b", base_url="http://localhost:11434/")

st.title('AI Assistant for Data Science 🤖')
st.write('''Hello :hand:, I'm AI Assistant and I'm here to help you with data science projects''')

with st.sidebar:
    st.write('*Your Data Science adventure begins with a CSV file.*')
    st.caption('**You may already know that every exciting data science journey starts with a dataset**')

    st.divider()

    st.caption("<p style = 'text-align:center'>Made By Me</p>", unsafe_allow_html=True)

# Button are not stateful. You can use the st.session_state object to create and manage session state varibles

# Initialise the key in session state
if 'clicked' not in st.session_state:
    st.session_state.clicked = {1:False}

def clicked(button):
    st.session_state.clicked[button]=True

st.button("Let's get started", on_click=clicked, args=[1])

if st.session_state.clicked[1]:
    st.header('Exploratory Data Analysis Part')
    st.subheader('Solution')
    
    user_csv = st.file_uploader("Upload your file here", type="csv")

    if user_csv is not None:
        user_csv.seek(0)
        df = pd.read_csv(user_csv, low_memory=False)

with st.sidebar:
    with st.expander('What are the steps of EDA'):
        st.write(llm('What are the steps of EDA'))

pandas_agent = create_pandas_dataframe_agent(llm, df, verbose=True)
question = 'What is the meaning of the columns'
columns_meaning = pandas_agent.run(question)
st.write(columns_meaning)