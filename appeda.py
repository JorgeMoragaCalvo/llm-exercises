import streamlit as st
import pandas as pd

from langchain_ollama import OllamaLLM
from langchain_experimental.agents import create_pandas_dataframe_agent

llm = OllamaLLM(model="llama3.2:latest", base_url="http://localhost:11434/")

st.title('AI Assistant for Data Science 🤖')
st.write('''Hello :hand:, I'm AI Assistant and I'm here to help you with data science projects''')

with st.sidebar:
    st.write('*Your Data Science adventure begins with a CSV file.*')
    st.caption('''**You may already know that every exciting data science journey starts with a dataset. That's 
               why I'd love for you to upload a CSV file**''')

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
        st.write(llm('In short, What are the steps of EDA'))

pandas_agent = create_pandas_dataframe_agent(llm, df, verbose=True, allow_dangerous_code=True)
#question = 'What is the meaning of the columns'
#columns_meaning = pandas_agent.invoke(question)
#st.write(columns_meaning)

def function_agent():
    st.write("**Data Overview**")
    st.write("The first rows of your dataset looks like this: ")
    st.write(df.head())
    st.write("**Data Cleaning**")
    columns_df = pandas_agent.invoke("What are the meaning of the columns?")
    st.write(columns_df)
    missing_values = pandas_agent.invoke("How many missing values does this dataframe have? Start the answer with 'There are'")
    st.write(missing_values)
    duplicates = pandas_agent.invoke("Are there any duplicate values and if so where?")
    st.write(duplicates)
    st.write("**Data summarisation**")
    st.write(df.describe())
    correlation_analysis = pandas_agent.invoke("Calculate correlations between numerical variables to identify potential relationships.")
    st.write(correlation_analysis)
    outliers = pandas_agent.invoke("Identify outliers in the data thay may be erroneous or that have a significant impact of the analysis.")
    st.write(outliers)
    new_features = pandas_agent.invoke("What new features would be interesting to create?")
    st.write(new_features)
    return

function_agent()