# RAG Data Pipeline

A fully local, end-to-end data pipeline that ingests Wikipedia data, generates vector embeddings, stores them in ChromaDB, and exposes a semantic search API — all using free and open-source tools.

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

---

## Tech Stack

* **FastAPI** – Backend API framework
* **Uvicorn** – ASGI server
* **ChromaDB** – Local persistent vector database
* **Sentence Transformers** – Embedding model (`all-MiniLM-L6-v2`)
* **PyTorch** – Model runtime
* **Wikipedia API** – Data source
* **LangChain Text Splitters** – Chunking
* **NumPy / tqdm** – Utilities

---

## Project Structure

```
rag-data-pipeline/
│
├── backend/
│   ├── app.py            # FastAPI app with /search, /health endpoints
│   ├── ingest.py         # Wikipedia fetch + chunk pipeline
│   ├── chunker.py        # Text splitting logic
│   ├── embedder.py       # Embedding generation (saves to data/embeddings/)
│   ├── vector_store.py   # Loads embeddings into ChromaDB
│   ├── search.py         # Query logic (embeds query → searches ChromaDB)
│   ├── requirements.txt
│   └── venv/             # Virtual environment
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

### 1. Create and activate virtual environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
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

Open the interactive docs at:

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health check — confirms API is running |
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

---

## Future Improvements

* Add LLM response generation (RAG completion)
* Add frontend UI (React / Next.js)
* Support multiple data sources (PDF, URLs)
* Add streaming responses

---

## Why this project?

This project showcases:

* End-to-end data pipeline design
* Vector databases & embeddings
* Backend API development with FastAPI
* Practical AI/ML system implementation

---

## License

MIT License
