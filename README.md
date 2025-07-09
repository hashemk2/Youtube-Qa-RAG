# YouTube Transcript QA RAG System

This project is a Question Answering (QA) system that leverages Retrieval-Augmented Generation (RAG) to answer questions about YouTube videos using their transcripts. It uses FastAPI for the backend, a modern web frontend, and integrates with state-of-the-art NLP models for semantic search and answer generation.

## Features
- Extracts transcripts from YouTube videos
- Splits and embeds transcript text for semantic search
- Uses FAISS for efficient vector search
- Generates answers using a large language model (LLM)
- Stores Q&A history in a SQLite database
- Simple and modern web interface

## Project Structure
```
requirements.txt
youtube_rag.db
README.md
app/
  backEnd/
    database.py        # Database models and session
    fastApi.py         # FastAPI backend server
    model.py           # Transcript processing, embedding, retrieval, and answer generation
  frontEnd/
    static/
      app.js           # Frontend JavaScript
      favicon.ico      # Favicon
      style.css        # CSS styles
    templates/
      index.html       # Main HTML template
```

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <https://github.com/hashemk2/Youtube-Qa-RAG.git>
cd "YouTube Transcript QA RAG System"
```

### 2. Install Python Dependencies
It is recommended to use a virtual environment.
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the Backend Server
```bash
uvicorn app.backEnd.fastApi:app --reload
```

### 4. Access the Web Interface
Open your browser and go to:  
`http://localhost:8000/`

## Usage
1. Enter a YouTube video URL and your question in the web form.
2. The system will extract the transcript, retrieve relevant context, and generate an answer using the LLM.
3. The answer and the Q&A history are stored in the database.

## Requirements
- Python 3.8+
- CUDA-enabled GPU recommended for LLM inference

## Main Python Packages Used
- fastapi
- uvicorn
- SQLAlchemy
- youtube-transcript-api
- langchain
- sentence-transformers
- faiss-cpu
- transformers
- torch

## Notes
- The LLM used is "TheBloke/Mistral-7B-Instruct-v0.2-GPTQ" (can be changed in `model.py`).
- For best performance, use a machine with a compatible GPU.
- The database is stored in `youtube_rag.db` (SQLite).

## License
MIT License

## Author
Hashem Abu Khalifah
