# RAG Data Pipeline

A fully local, end-to-end data pipeline that ingests Wikipedia data, generates vector embeddings, stores them in ChromaDB, exposes a semantic search API, and includes a React frontend — all using free and open-source tools.

---

## Overview

This project demonstrates how to build a simple **RAG-style (Retrieval-Augmented Generation) pipeline** without relying on paid APIs.

It:

* Fetches data from Wikipedia
* Splits text into chunks
* Generates embeddings locally using `all-MiniLM-L6-v2`
* Saves embeddings to disk as JSON
* Stores them in a local ChromaDB vector database
* Exposes a semantic search API via FastAPI
* Provides a React + Vite frontend for natural language search

---

## Tech Stack

**Backend**
* **FastAPI** – Backend API framework
* **Uvicorn** – ASGI server
* **ChromaDB** – Local persistent vector database
* **Sentence Transformers** – Embedding model (`all-MiniLM-L6-v2`)
* **PyTorch** – Model runtime
* **Wikipedia API** – Data source
* **LangChain Text Splitters** – Chunking
* **NumPy / tqdm** – Utilities

**Frontend**
* **React 19** – UI framework
* **Vite** – Dev server and build tool

---

## Project Structure

```
rag-data-pipeline/
│
├── backend/
│   ├── app.py            # FastAPI app with /search, /health endpoints + CORS
│   ├── ingest.py         # Wikipedia fetch + chunk pipeline
│   ├── chunker.py        # Text splitting logic
│   ├── embedder.py       # Embedding generation (saves to data/embeddings/)
│   ├── vector_store.py   # Loads embeddings into ChromaDB
│   ├── search.py         # Query logic (embeds query → searches ChromaDB)
│   ├── requirements.txt
│   └── venv/             # Virtual environment
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx       # Search UI — query input, top-k selector, results
│   │   ├── App.css       # Styles
│   │   └── main.jsx      # React entry point
│   ├── public/
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
├── data/
│   ├── raw/              # Raw Wikipedia text
│   ├── processed/        # Chunked text as JSON
│   ├── embeddings/       # Generated embedding JSON files
│   └── chroma_db/        # Persistent ChromaDB vector store
│
└── README.md
```

---

## Setup Instructions

### Backend

#### 1. Create and activate virtual environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

#### 2. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Frontend

#### 3. Install frontend dependencies

```bash
cd frontend
npm install
```

---

## Running the Pipeline

Run each step from inside the `backend/` directory with the virtual environment activated.

### Step 1 — Ingest Wikipedia data and chunk it

```bash
python ingest.py
```

Fetches Wikipedia articles, splits them into chunks, and saves to `data/processed/`.

### Step 2 — Generate embeddings

```bash
python embedder.py
```

Loads chunks from `data/processed/`, generates embeddings using `all-MiniLM-L6-v2`, and saves to `data/embeddings/`.

### Step 3 — Store embeddings in ChromaDB

```bash
python vector_store.py
```

Reads embedding JSON files and inserts them into a local ChromaDB collection (`wiki_articles`) persisted at `data/chroma_db/`.

### Step 4 — Start the API server

```bash
uvicorn app:app --reload
```

API runs at `http://127.0.0.1:8000`. Interactive docs at:

```
http://127.0.0.1:8000/docs
```

### Step 5 — Start the frontend

```bash
cd frontend
npm run dev
```

Frontend runs at `http://localhost:5173`.

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Confirms API is running |
| `GET` | `/health` | Returns `{"status": "healthy"}` |
| `GET` | `/search?q=...&top_k=5` | Semantic search over stored Wikipedia chunks |

### Example search query

```
GET /search?q=What is a vector database?&top_k=5
```

Response:

```json
{
  "query": "What is a vector database?",
  "top_k": 5,
  "results": [
    {
      "id": "chunk_id",
      "text": "...",
      "metadata": { "article": "Vector database" },
      "distance": 0.21
    }
  ]
}
```

---

## Features

* 100% free and local (no paid APIs)
* Modular pipeline — each stage is an independent script
* Semantic search using dense vector embeddings
* Persistent ChromaDB storage — no re-ingestion needed between runs
* FastAPI with auto-generated Swagger UI at `/docs`
* CORS enabled for local frontend development
* React frontend with natural language search, top-k selector, and result cards

---

## Backend Changes (this branch)

* **CORS middleware** added to `app.py` — allows requests from `http://localhost:5173` and `http://127.0.0.1:5173` (Vite dev server)
* **Defensive error handling** in `vector_store.py` — raises a clear `FileNotFoundError` with instructions if the embeddings directory is missing instead of crashing silently

---

## Why this project?

This project showcases:

* End-to-end data pipeline design
* Vector databases & embeddings
* Backend API development with FastAPI
* Frontend integration with React + Vite
* Practical AI/ML system implementation

---

## License

MIT License
