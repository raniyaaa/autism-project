import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


from dotenv import load_dotenv
import os
load_dotenv()

# Initialize Flask App
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configure Logging
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

# Groq API Key (Replace with your actual key)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize AI components
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = None
chat_history = []
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)

@app.route("/upload", methods=["POST"])
def upload_pdfs():
    """Handles PDF file uploads, extracts text, and creates vector embeddings."""
    global vectorstore
    all_text = ""

    if "pdfs" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    files = request.files.getlist("pdfs")

    for file in files:
        try:
            reader = PdfReader(file)
            for page in reader.pages:
                all_text += page.extract_text() or ""  # Avoid NoneType errors
        except Exception as e:
            logging.error(f"Error processing {file.filename}: {e}")
            return jsonify({"error": f"Failed to process {file.filename}"}), 500

    try:
        text_chunks = text_splitter.split_text(all_text)
        vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embedding_model)
        return jsonify({"message": "PDF uploaded and processed successfully!", "chunks": len(text_chunks)})
    except Exception as e:
        logging.error(f"Error creating vector store: {e}")
        return jsonify({"error": "Failed to create vector store"}), 500

@app.route("/query", methods=["POST"])
def query():
    """Handles user queries using the AI model and vectorized PDF content."""
    global chat_history
    data = request.json
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"error": "Query cannot be empty"})
    print(user_query)
    memory_length = 15
    try:
        context = ""
        if vectorstore:
            results = vectorstore.similarity_search(user_query, k=3)
            context = "\n".join([doc.page_content for doc in results])

        full_query = f"Relevant Context:\n{context}\n\nUser Query:\n{user_query}"
        system_message = (
            "You are a helpful assistant who only answers questions related to autism, ASD, neurodiversity, "
            "treatments, support strategies, and related topics. If the user's question is not about autism, "
            "politely refuse to answer."
        )
        # Setup conversation memory
        memory = ConversationBufferWindowMemory(k=memory_length)
        memory.save_context({"input":system_message}, {"output":""})
        for message in chat_history:
            memory.save_context({"input": message["human"]}, {"output": message["AI"]})

        # Initialize Groq AI Model
        groq_chat = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="qwen-2.5-32b")



        conversation = ConversationChain(llm=groq_chat, memory=memory)
        response = conversation(full_query)

        chat_history.append({"human": user_query, "AI": response["response"]})

        return jsonify({"response": response["response"]})
    except Exception as e:
        logging.error(f"Error processing query: {e}")
        return jsonify({"error": "Failed to process query"}), 500

# Run Flask Server
if __name__ == "__main__":
    print('Gonna run it now')
    app.run(debug=True)
