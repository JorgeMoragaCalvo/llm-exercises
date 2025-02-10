import streamlit as st
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

st.markdown("""
    <style>
    .stApp {
            background-color: #0E1117;
            color: #FFFFFF;
            }
    .stChatInput input {
            background-color: #01E1E1E !important;
            color: #FFFFFF !important;
            border: 1px solid #3A3A3A !important;
            }
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd){
            background-color: #1E1E1E !important;
            color: #E0E0E0 !important;
            border: 1px solid #3A3A3A !important;
            border-radius: 10px;
            padding: 15px;
            marging: 10px 0;
            }
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even){
            background-color: #02A2A2A !important;
            color: #F0F0F0 !important;
            border: 1px solid #404040 !important;
            border-radius: 10px;
            padding: 15px;
            marging: 10px 0;
            }
    .stChatMessage .avatar {
            background-color: #00FFAA !important
            color: #000000 !important;
            }
    .stChatMessage p, .stChatMessage div {
            color: #FFFFFF !important;
            }
    .stFileUploader {
            background-color: #01E1E1E;
            border: 1px solid #3A3A3A;
            border-radius: 5px;
            padding: 15px;
            }
    h1, h2, h3 {
            color: #00FFAA !important
            }
    </style>
""", unsafe_allow_html=True)

PROMP_TEMPLATE = """
You are an expert research assistant. Use the provided context to answer the query.
If unsure, state you don't know. Be concise and factual (max 3 sentences).

Query: {user_query}
Context: {document_context}
Answer:
"""
PDF_STORE_PATH = 'document_store/pdfs/'
EMBEDDING_MODEL = OllamaEmbeddings(model="llama3.2:latest")
DOCUMENT_VECTOR_DB = InMemoryVectorStore(EMBEDDING_MODEL)
LANGUAGE_MODEL = OllamaLLM(model="llama3.2:latest")

def save_uploaded_file(uploaded_file):
    file_path = PDF_STORE_PATH + uploaded_file.name
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())
    return file_path

def load_pdf_documents(file_path):
    document_loader = PDFPlumberLoader(file_path)
    return document_loader.load()

def chunk_documents(raw_documents):
    text_processor = RecursiveCharacterTextSplitter(
        chunk_size = 100,
        chunk_overlap=10,
        add_start_index=True
    )
    return text_processor.split_documents(raw_documents)

def index_documents(document_chunks):
    DOCUMENT_VECTOR_DB.add_documents(document_chunks)

def find_related_documents(query):
    return DOCUMENT_VECTOR_DB.similarity_search(query)

def generate_answer(user_query, context_documents):
    context_text = "\n\n".join([doc.page_content for doc in context_documents])
    conversation_prompt = ChatPromptTemplate.from_template(PROMP_TEMPLATE)
    response_chain = conversation_prompt | LANGUAGE_MODEL
    return response_chain.invoke({"user_query": user_query, "document_context": context_text})

# UI

st.title("📘 DocuMind AI")
st.markdown("### Your Intelligent Document Assistant")
st.markdown("---")

uploaded_file = st.file_uploader(
    "Upload Research Document (PDF)",
    type="pdf",
    help="Select a PDF document for analysis",
    accept_multiple_files=False
)

if uploaded_file:
    saved_path = save_uploaded_file(uploaded_file)
    raw_docs = load_pdf_documents(saved_path)
    processed_chunks = chunk_documents(raw_docs)
    index_documents(processed_chunks)

    st.success("Document processed succesfully! Ask your questions bellow")

    user_input = st.chat_input("Enter your question about the document...")

    if user_input:
        with st.chat_message("user"):
            st.write(user_input)
        
        with st.spinner("Analyzind document..."):
            relevant_docs = find_related_documents(user_input)
            ai_response = generate_answer(user_input, relevant_docs)
        
        with st.chat_message("assistant", avatar="🤖"):
            st.write(ai_response)