# Autism Project
This project helps users detect signs of autism by analyzing user responses and PDF content related to Autism Spectrum Disorder (ASD). It uses a pretrained language model (Qwen-2.5 via Groq API) and vector-based search (FAISS + HuggingFace embeddings) to answer queries based on uploaded research papers or medical documents

## Features
- Upload one or multiple PDFs (research papers, documents, etc.)
- Extracts and vectorizes the content for efficient semantic search
- Chatbot powered by LangChain + Groq API (Qwen-2.5-32B)
- Remembers recent conversation context using memory buffers
- Strict domain filtering: only answers questions related to autism, neurodiversity, and related medical/social aspects
## Tech Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **ML Model**: Pretrained classifier
- **LLM**: Groq API (qwen-2.5-32b
- **PDF Parsing**: PYPDF2
- **Memory Management**: LangChain ConversationBufferWindowMemory
## Files Overview
- `index.html` – User interface for taking input
- `styles.css` – Styling for the web page
- `script.js` – Handles user interactions
- `back.py` / `vector.py` – Backend ML processing
- `requirement.txt` – Dependencies for Python backend
## Note
  Due to time constraints, a pretrained model was used instead of training one from scratch.

    
