# main.py

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate

# IMPORTS for FastAPI
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.staticfiles import StaticFiles

# --- Configuration ---
load_dotenv()

# --- 1. One-Time Setup ---

print("--- Starting Server Setup ---")

def load_all_documents(folder_path: str = "."):
    all_documents = []
    print(f"Scanning for documents in: {os.path.abspath(folder_path)}")
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith(".pdf"):
            print(f" > Loading PDF: {filename}")
            loader = PyPDFLoader(file_path)
            all_documents.extend(loader.load())
        elif filename.endswith(".txt"):
            print(f" > Loading TXT: {filename}")
            loader = TextLoader(file_path, encoding='utf-8-sig')
            all_documents.extend(loader.load())
    print(f"\nTotal documents loaded: {len(all_documents)}")
    return all_documents

def split_documents(documents):
    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    print(f"Total chunks created: {len(chunks)}")
    return chunks

def create_vector_store(text_chunks):
    print("Creating vector store with OpenAI embeddings...")
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(text_chunks, embeddings)
    print("Vector store created successfully.")
    return vectorstore

prompt_template = """You are a Socratic dialogue agent. Your purpose is not just to answer questions, but to stimulate deeper philosophical thought.

Based on the following context from ancient philosophical texts, first, provide a concise and direct answer to the user's question.
Then, you MUST end your response by asking a thought-provoking, open-ended question that is related to the user's original query, guiding them to explore the topic more deeply.

CONTEXT:
{context}

USER'S QUESTION:
{question}

SOCRATIC RESPONSE (Answer, followed by a question):"""
prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

def create_retrieval_chain(vectorstore, prompt):
    print("Creating the retrieval chain...")
    chain_type_kwargs = {"prompt": prompt}
    qa_chain = RetrievalQA.from_chain_type(
        llm=OpenAI(),
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        return_source_documents=True,
        chain_type_kwargs=chain_type_kwargs
    )
    print("Retrieval chain ready.")
    return qa_chain

# --- Execute the setup process ---
documents = load_all_documents("spiritual_database")
text_chunks = split_documents(documents)
vectorstore = create_vector_store(text_chunks)
socratic_chain = create_retrieval_chain(vectorstore, prompt)

print("--- Server Setup Complete. API is Ready. ---")

# --- 2. API Definition ---
app = FastAPI(
    title="Socratic Dialogue Agent API",
    description="An API for interacting with a RAG-based philosophical agent.",
    version="1.0.0",
)

# --- Define API Routes First ---
class QuestionRequest(BaseModel):
    question: str

class SourceDocument(BaseModel):
    page_content: str
    metadata: dict

class AnswerResponse(BaseModel):
    answer: str
    sources: List[SourceDocument]

@app.post("/ask")
def ask_question(request: QuestionRequest):
    print(f"Received question: {request.question}")
    response = socratic_chain.invoke(request.question)
    
    return {
        "answer": response['result'],
        "sources": response['source_documents']
    }

# --- FIX: MOUNT STATIC FILES LAST ---
# Now that our specific API routes are defined, we add the catch-all for our frontend.
app.mount("/", StaticFiles(directory="static", html=True), name="static")