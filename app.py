# Importing the necessary libraries
import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import ChatCohere
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain

# Loading the environment variables
load_dotenv()

# Directory for storing the uploaded files
temp_dir = r"./temp_dir"

# Extract the text content from the files


def extract_text(files):
    docs = []

    for file in files:
        file_path = temp_dir+'/'+file.name
        with open(file_path, "wb") as f:
            f.write(file.read())

        if file_path.endswith(".pdf"):
            docs.extend(PyPDFLoader(file_path).load())

        elif file_path.endswith(".txt"):
            docs.extend(TextLoader(file_path, encoding="utf8").load())

        elif file_path.endswith(".doc") or file_path.endswith(".docx"):
            docs.extend(Docx2txtLoader(file_path).load())
        else:
            pass
    return docs

# Split the documents into chunks


def split_to_chunks(docs):
    docs = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200).split_documents(docs)
    return docs

# Convert to vector embeddings and store in vector database


def vector_store(docs):
    vectordb = Chroma.from_documents(docs, embedding=HuggingFaceEmbeddings())
    return vectordb


# Creating User Interface with streamlit
st.set_page_config("Document Chatbot")
st.title("Document based chatbot")

user_query = st.text_input("User Input: ", placeholder="Enter your question")
ask_button = st.button("Ask")

with st.sidebar:
    uploaded_docs = st.file_uploader(
        label="Upload Documents", type=["pdf", "docx", "doc", "txt"], accept_multiple_files=True)

if uploaded_docs and ask_button:
    with st.spinner("Generating response . . ."):
        # Loading the documents and extracting the text content
        docs = extract_text(uploaded_docs)

        # Splitting the documents into chunks
        docs = split_to_chunks(docs)

        # Embedding into vector and storing the vectors in a Vector Store
        vectordb = vector_store(docs)

        # create our Q&A retreieval chain
        qa_chain = ConversationalRetrievalChain.from_llm(
            ChatCohere(temperature=0.5),
            retriever=vectordb.as_retriever(
                search_kwargs={'k': 3}),
            return_source_documents=True,
            verbose=False
        )

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        result = qa_chain(
            {"question": user_query, "chat_history": st.session_state.chat_history})
        st.session_state.chat_history.append((user_query, result["answer"]))
        st.write(":robot_face: Chatbot:  " + result["answer"])
        print(st.session_state.chat_history)
