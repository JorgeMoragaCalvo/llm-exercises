import tempfile
from langchain_ollama import OllamaLLM
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain

import streamlit as st

# # Configuración de Streamlit
# st.set_page_config(page_title="Chat PDF con IA", layout="wide")
# st.title("📄💬 Chat con tu PDF usando LangChain + Ollama")

# # 1️⃣ Subir el archivo PDF
# pdf_file = st.file_uploader("📂 Sube un archivo PDF", type="pdf")

# # 2️⃣ Procesar el PDF y generar embeddings
# if pdf_file:
#     with st.spinner("🔄 Procesando PDF..."):
#         loader = PyPDFLoader(pdf_file)
#         docs = loader.load()
#         text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#         split_docs = text_splitter.split_documents(docs)

#         embeddings = OllamaEmbeddings(model="mistral")
#         vector_store = FAISS.from_documents(split_docs, embeddings)

#         retriever = vector_store.as_retriever()
        
#         # 3️⃣ Definir un prompt seguro
#         custom_prompt = PromptTemplate(
#             template="""
#             Responde únicamente con información basada en el documento proporcionado.
#             Si la pregunta no está en el documento, responde: "No encontré información sobre eso en el documento."

#             Documento: {context}

#             Pregunta: {question}
#             """,
#             input_variables=["context", "question"],
#         )

#         # 4️⃣ Configurar el modelo y la cadena de QA
#         llm = OllamaLLM(model="mistral")
#         qa_chain = create_retrieval_chain.from_chain_type(
#             llm, retriever=retriever, chain_type_kwargs={"prompt": custom_prompt}
#         )

#         st.success("✅ PDF procesado. ¡Listo para hacer preguntas!")

#         # 5️⃣ Manejar el chat interactivo
#         if "messages" not in st.session_state:
#             st.session_state.messages = []

#         # Mostrar historial del chat
#         for message in st.session_state.messages:
#             with st.chat_message(message["role"]):
#                 st.markdown(message["content"])

#         # Entrada de usuario
#         pregunta = st.chat_input("Escribe tu pregunta sobre el documento...")

#         if pregunta:
#             st.session_state.messages.append({"role": "user", "content": pregunta})
#             with st.chat_message("user"):
#                 st.markdown(pregunta)

#             with st.chat_message("assistant"):
#                 with st.spinner("Pensando... 🤖"):
#                     respuesta = qa_chain.run(pregunta)
#                     st.markdown(respuesta)

#             st.session_state.messages.append({"role": "assistant", "content": respuesta})


# Configuración de Streamlit
st.set_page_config(page_title="Chat PDF con IA", layout="wide")
st.title("📄💬 Chat con tu PDF usando LangChain + Ollama")

# 1️⃣ Subir el archivo PDF
pdf_file = st.file_uploader("📂 Sube un archivo PDF", type="pdf")

# 2️⃣ Procesar el PDF y generar embeddings
if pdf_file:
    with st.spinner("🔄 Procesando PDF..."):
        try:
            # Guardar el archivo PDF en un archivo temporal
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(pdf_file.read())
                tmp_file_path = tmp_file.name

            # Cargar el PDF usando PyPDFLoader
            loader = PyPDFLoader(tmp_file_path)
            docs = loader.load()
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            split_docs = text_splitter.split_documents(docs)

            embeddings = OllamaEmbeddings(model="deepseek-r1:1.5b", base_url="http://localhost:11434/")
            vector_store = FAISS.from_documents(split_docs, embeddings)

            retriever = vector_store.as_retriever()
            
            # 3️⃣ Definir un prompt seguro
            custom_prompt = PromptTemplate(
                template="""
                Responde únicamente con información basada en el documento proporcionado.
                Si la pregunta no está en el documento, responde: "No encontré información sobre eso en el documento."

                Documento: {context}

                Pregunta: {question}
                """,
                input_variables=["context", "question"],
            )

            # 4️⃣ Configurar el modelo y la cadena de QA
            llm = OllamaLLM(model="mistral")
            qa_chain = load_qa_chain(
                llm, retriever=retriever, chain_type_kwargs={"prompt": custom_prompt}
            )

            st.success("✅ PDF procesado. ¡Listo para hacer preguntas!")

            # 5️⃣ Manejar el chat interactivo
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # Mostrar historial del chat
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Entrada de usuario
            pregunta = st.chat_input("Escribe tu pregunta sobre el documento...")

            if pregunta:
                st.session_state.messages.append({"role": "user", "content": pregunta})
                with st.chat_message("user"):
                    st.markdown(pregunta)

                with st.chat_message("assistant"):
                    with st.spinner("Pensando... 🤖"):
                        respuesta = qa_chain.run(pregunta)
                        st.markdown(respuesta)

                st.session_state.messages.append({"role": "assistant", "content": respuesta})
        except Exception as e:
            st.error(f"Error al procesar el PDF: {e}")

# def load_pdf(pdf_path):
#     loader = PyPDFLoader(pdf_path)
#     docs = loader.load()
#     text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     splits_docs = text_splitter.split_documents(docs)
#     return splits_docs

# def create_vector_store(docs):
#     embeddings = OllamaEmbeddings(model="deepseek-r1:1.5b", base_url="http://localhost:11434/")
#     vector_store = FAISS.from_documents(docs, embeddings)
#     return vector_store

# def setup_qa_chain(vector_store):
#     llm = OllamaLLM(model="deepseek-r1:1.5b", base_url="http://localhost:11434/")
#     retriever = vector_store.as_retriever()

#     custom_prompt = PromptTemplate(
#         template = """
#         Answer only based in document information.
#         If the question is not within document, answer: "No encontré información sobre eso en el documento."

#         Document: {context}

#         Question: {question}
#         """,
#         input_variables=["context", "question"],
#     )

#     qa_chain = create_retrieval_chain.from_chain_type(
#         llm, 
#         retriever=retriever,
#         chain_type_kwargs={"prompt": custom_prompt})
#     return qa_chain

# def main():
#     pdf_path = "FilosofiaDeLaBiologiaBiologiaDelConocimientoYBiote.pdf"
#     docs = load_pdf(pdf_path)
#     vector_store = create_vector_store(docs)
#     qa_chain = setup_qa_chain(vector_store)

#     while True:
#         query = input("\n❓ Question (or write 'out' to finish): ")
#         if query.lower() == "out":
#             break
#         answer = qa_chain.run(query)
#         print("Answer: ", answer)

# if __name__ == "__main__":
#     main()