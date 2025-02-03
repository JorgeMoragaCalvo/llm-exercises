import streamlit as st
from langchain_ollama import ChatOllama

st.title("🧠 This a Simple Chat Application with Ollama/DeeSeek and Langchain!")
#st.write("GET MORE INFO @ KGP Talkie: https://www.youtube.com/kgptalkie")

with st.form("llm-form"):
    text = st.text_area("Enter your question:")
    submit = st.form_submit_button("Submit")

def generate_response(input_text):
    model = ChatOllama(model="deepseek-r1:1.5b", base_url="http://localhost:11434/")

    response = model.invoke(input_text)

    return response.content

if "chat_history" not in st.session_state:
    st.session_state['chat_history'] = []

if submit and text:
    with st.spinner("Generating response..."):
        response = generate_response(text)
        st.session_state['chat_history'].append({"user": text, "ollama": response})
        st.write(response)

st.write("## Chat History")
for chat in reversed(st.session_state['chat_history']):
    st.write(f"** 🧑 User**: {chat['user']}")
    st.write(f"**🧠 Assistant**: {chat['ollama']}")
    st.write("---")