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
│   ├── app.py            # FastAPI app — /search, /health endpoints + CORS
│   ├── ingest.py         # Wikipedia fetch + chunk pipeline
│   ├── chunker.py        # Text splitting logic
│   ├── embedder.py       # Embedding generation (saves to data/embeddings/)
│   ├── vector_store.py   # Loads embeddings into ChromaDB
│   ├── search.py         # Query logic — embeds query and searches ChromaDB
│   ├── requirements.txt
│   └── venv/             # Virtual environment (not committed)
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx       # Search UI — query input, top-k selector, result cards
│   │   ├── App.css       # Styles
│   │   └── main.jsx      # React entry point
│   ├── public/
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
├── data/                 # Generated at runtime — not committed
│   ├── raw/              # Raw Wikipedia text
│   ├── processed/        # Chunked text as JSON
│   ├── embeddings/       # Generated embedding JSON files
│   └── chroma_db/        # Persistent ChromaDB vector store
│
└── README.md
```

---

## Setup

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

---

## Running the Pipeline

Run each step from inside the `backend/` directory with the virtual environment activated.

### Step 1 — Ingest Wikipedia data

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

API runs at `http://127.0.0.1:8000`. Interactive Swagger docs at `http://127.0.0.1:8000/docs`.

### Step 5 — Start the frontend

```bash
cd frontend
npm run dev
```

Frontend runs at `http://localhost:5173`.

---

## API Reference

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Confirms API is running |
| `GET` | `/health` | Returns `{"status": "healthy"}` |
| `GET` | `/search` | Semantic search over stored Wikipedia chunks |

### `GET /search`

**Query parameters**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `q` | string | Yes | — | Natural language search query |
| `top_k` | integer | No | `5` | Number of results to return |

### Sample queries

```
GET /search?q=How does machine learning work?&top_k=3
GET /search?q=What is a vector database?&top_k=5
GET /search?q=How is AI related to cloud computing?&top_k=5
GET /search?q=What are transformers in NLP?&top_k=3
GET /search?q=Explain neural networks&top_k=5
```

### Example response

```bash
curl "http://127.0.0.1:8000/search?q=What+is+a+vector+database%3F&top_k=2"
```

```json
{
  "query": "What is a vector database?",
  "top_k": 2,
  "results": [
    {
      "id": "vector_database_chunk_0",
      "text": "A vector database is a type of database that stores data as high-dimensional vectors, which are mathematical representations of features or attributes...",
      "metadata": {
        "article": "vector database"
      },
      "distance": 0.1842
    },
    {
      "id": "vector_database_chunk_3",
      "text": "Vector databases are used in a variety of applications including recommendation systems, image search, natural language processing, and anomaly detection...",
      "metadata": {
        "article": "vector database"
      },
      "distance": 0.2317
    }
  ]
}
```

**Distance** is a cosine distance score — lower values indicate higher semantic similarity.

---

## Features

* 100% free and local — no paid APIs
* Modular pipeline — each stage is an independent script
* Semantic search using dense vector embeddings
* Persistent ChromaDB storage — no re-ingestion needed between runs
* FastAPI with auto-generated Swagger UI at `/docs`
* CORS enabled for local frontend development
* React frontend with natural language search, top-k selector, and result cards

---

## Why this project?

This project showcases:

* End-to-end data pipeline design
* Vector databases and embeddings
* Backend API development with FastAPI
* Frontend integration with React + Vite
* Practical AI/ML system implementation

---

## License

MIT License
