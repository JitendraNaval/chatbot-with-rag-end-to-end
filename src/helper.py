import os
import sys
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer


# Extract Data from the pdf file
def load_pdf_file(directory_path:str):
    """Loads all PDF files from a given directory."""
    loader=DirectoryLoader(directory_path,glob="*.pdf",loader_cls=PyPDFLoader)
    documents=loader.load()
    return documents


#Split the Data into Text Chunks

def split_text(documents, chunk_size=500, chunk_overlap=20):
    """Splits text into chunks for processing."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    text_chunks = text_splitter.split_documents(documents)
    return text_chunks

def download_hugging_face_embedding():
    """Downloads and returns Hugging Face embeddings."""
    model_name = "sentence-transformers/all-mpnet-base-v2"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)
   # embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    return embeddings

