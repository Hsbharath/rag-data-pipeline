# RAG Data Pipeline

A fully local, end-to-end data pipeline that ingests Wikipedia data, generates vector embeddings, stores them in ChromaDB, exposes a semantic search API, and includes a React frontend — all using free and open-source tools.

---

## Demo

https://github.com/user-attachments/assets/2d86df2a-bad0-4447-bf5a-3a8c7fbdebdd

> Search Wikipedia knowledge with semantic retrieval and local RAG answer generation — no paid APIs required.

---

## Overview

This project demonstrates how to build a simple **RAG-style (Retrieval-Augmented Generation) pipeline** without relying on paid APIs.

It:

* Fetches data from Wikipedia
* Splits text into chunks
* Generates embeddings locally using `all-MiniLM-L6-v2`
* Saves embeddings to disk as JSON
* Stores them in a local ChromaDB vector database
* Exposes a semantic search API via FastAPI with two modes: **Semantic Retrieval** and **RAG Answer**
* Provides a React + Vite frontend for natural language search

---

## Search Modes

The `/search` endpoint supports two modes, selectable from the frontend via radio buttons.

### Semantic Retrieval (default)

Returns the top-k most similar text chunks from ChromaDB based on vector similarity to the query. No text is generated — results are the raw stored chunks ranked by cosine distance.

Use this when you want to explore what the vector database contains or when you need full control over the raw results.

### RAG Answer

Retrieves the top-k chunks from ChromaDB and passes them as context to a local text generation model (`google/flan-t5-base`). The model synthesises a natural language answer grounded in those chunks.

The response includes:
* A generated `answer` string
* The `source_chunks` used to produce it (same shape as Semantic Retrieval results)

**Detail level** controls how the answer is generated:
* `low` — concise, 1–2 sentence answer (~100 tokens)
* `high` — thorough, elaborated answer (~500 tokens)

Use this when you want a direct, synthesised answer rather than raw document fragments.

---

## Tech Stack

**Backend**
* **FastAPI** – Backend API framework
* **Uvicorn** – ASGI server
* **ChromaDB** – Local persistent vector database
* **Sentence Transformers** – Embedding model (`all-MiniLM-L6-v2`)
* **Transformers (Hugging Face)** – Local generation model (`flan-t5-base`) for RAG mode
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
│   ├── rag.py            # RAG answer generation using flan-t5-base
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
│   │   ├── App.jsx       # Search UI — query input, mode selector, result cards
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
├── video/
│   └── wikivector_search.mov   # Demo recording
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

> **Note:** The first startup downloads `all-MiniLM-L6-v2` (~90 MB) for embeddings and `flan-t5-base` (~990 MB) for RAG generation. Both are cached locally by Hugging Face after the first download.

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
| `GET` | `/search` | Semantic search or RAG answer over stored Wikipedia chunks |

### `GET /search`

**Query parameters**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `q` | string | Yes | — | Natural language search query |
| `top_k` | integer | No | `5` | Number of chunks to retrieve |
| `mode` | string | No | `semantic` | `semantic` returns raw chunks; `rag` returns a generated answer |
| `detail` | string | No | `high` | Only applies when `mode=rag`. `low` = concise (~100 tokens); `high` = detailed (~500 tokens) |

### Sample queries

```
GET /search?q=How does machine learning work?&top_k=3
GET /search?q=What is a vector database?&mode=rag&top_k=5
GET /search?q=What is a vector database?&mode=rag&detail=low&top_k=5
GET /search?q=How is AI related to cloud computing?&mode=semantic&top_k=5
GET /search?q=What are transformers in NLP?&mode=rag&detail=high&top_k=3
```

### Example response — Semantic Retrieval

```bash
curl "http://127.0.0.1:8000/search?q=What+is+a+vector+database%3F&top_k=2"
```

```json
{
  "query": "What is a vector database?",
  "top_k": 2,
  "mode": "semantic",
  "results": [
    {
      "id": "vector_database_chunk_0",
      "text": "A vector database is a type of database that stores data as high-dimensional vectors...",
      "metadata": { "article": "vector database" },
      "distance": 0.1842
    },
    {
      "id": "vector_database_chunk_3",
      "text": "Vector databases are used in a variety of applications including recommendation systems...",
      "metadata": { "article": "vector database" },
      "distance": 0.2317
    }
  ]
}
```

### Example response — RAG Answer

```bash
curl "http://127.0.0.1:8000/search?q=What+is+a+vector+database%3F&top_k=2&mode=rag&detail=high"
```

```json
{
  "query": "What is a vector database?",
  "top_k": 2,
  "mode": "rag",
  "detail": "high",
  "answer": "A vector database stores data as high-dimensional vectors and is used in applications such as recommendation systems, image search, and natural language processing.",
  "source_chunks": [
    {
      "id": "vector_database_chunk_0",
      "text": "A vector database is a type of database that stores data as high-dimensional vectors...",
      "metadata": { "article": "vector database" },
      "distance": 0.1842
    },
    {
      "id": "vector_database_chunk_3",
      "text": "Vector databases are used in a variety of applications including recommendation systems...",
      "metadata": { "article": "vector database" },
      "distance": 0.2317
    }
  ]
}
```

**Distance** is a cosine distance score — lower values indicate higher semantic similarity.

---

## Features

* 100% free and local — no paid APIs
* Two search modes: raw chunk retrieval and generated natural language answers
* Configurable RAG answer detail — concise (~100 tokens) or detailed (~500 tokens)
* Modular pipeline — each stage is an independent script
* Semantic search using dense vector embeddings
* Persistent ChromaDB storage — no re-ingestion needed between runs
* FastAPI with auto-generated Swagger UI at `/docs`
* CORS enabled for local frontend development
* React frontend with natural language search, top-k selector, mode toggle, detail level selector, and result cards

---

## Why this project?

This project showcases:

* End-to-end data pipeline design
* Vector databases and embeddings
* Retrieval-Augmented Generation (RAG) with local models
* Backend API development with FastAPI
* Frontend integration with React + Vite
* Practical AI/ML system implementation

---

## License

MIT License
