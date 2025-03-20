import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from src.store_index import create_vector_store
from src.Prompt import system_prompt
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("GROQ_API_KEY is missing. Please set it in your environment variables.")
    st.stop()

# Initialize chatbot model
model = ChatGroq(model="llama3-8b-8192")

# Load vector store
vectorstore = create_vector_store('C:\\Users\\jeetu\\Desktop\\chatbot\\Data\\')
retriever = vectorstore.as_retriever()

# Setup chat prompt
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{query}"),  
])

# Initialize RAG-based retrieval chain
rag_chain = RetrievalQA.from_chain_type(llm=model, retriever=retriever, chain_type="stuff")

# Streamlit UI
def main():
    st.title("AI-Powered Chatbot")
    st.write("Ask questions based on the provided PDFs.")

    # Initialize session state to store chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # User input field
    user_input = st.text_input("Your Question:")

    if user_input:
        try:
            response = rag_chain.invoke({"query": user_input})  
            answer = response.get("result", "Sorry, I couldn't find an answer.")

            # Store question and answer in chat history
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("AI", answer))

        except Exception as e:
            st.session_state.chat_history.append(("AI", f"Error: {str(e)}"))

    # Display chat history
    for role, text in st.session_state.chat_history:
        if role == "You":
            st.markdown(f"**{role}:** {text}")
        else:
            st.markdown(f"**{role}:** {text}", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
