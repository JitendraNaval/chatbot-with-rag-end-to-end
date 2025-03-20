from langchain_chroma import Chroma
from src.helper import load_pdf_file, split_text, download_hugging_face_embedding

def create_vector_store(data_path: str):
    """Loads PDF data, processes it, and stores embeddings in a vector store."""
    documents = load_pdf_file(data_path)
    text_chunks = split_text(documents)
    embeddings = download_hugging_face_embedding()
    vectorstore = Chroma.from_documents(documents=text_chunks, embedding=embeddings)
    return vectorstore
