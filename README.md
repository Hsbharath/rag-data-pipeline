# RAG Data Pipeline

A fully local, end-to-end data pipeline that ingests online data, generates vector embeddings, and enables semantic search — all using free and open-source tools.

---

## Overview

This project demonstrates how to build a simple **RAG-style (Retrieval-Augmented Generation) pipeline** without relying on paid APIs.

It:

* Fetches data from Wikipedia
* Splits text into chunks
* Generates embeddings locally
* Stores them in a vector database
* Exposes a search API for semantic queries

---

## Tech Stack

* **FastAPI** – Backend API
* **Uvicorn** – ASGI server
* **ChromaDB** – Local vector database
* **Sentence Transformers** – Embedding model
* **PyTorch** – Model runtime
* **Wikipedia API** – Data source
* **LangChain Text Splitters** – Chunking
* **NumPy / tqdm** – Utilities

---

## Project Structure

```
free-data-pipeline/
│
├── backend/
│   ├── app.py        # FastAPI app
│   ├── ingest.py     # Data ingestion + embedding pipeline
│   ├── search.py     # Query logic
│   ├── chunker.py    # Text splitting
│   ├── requirements.txt
│   └── chroma_db/    # Local vector store
│
├── data/
│   ├── raw/
│   └── processed/
│
└── README.md
```

---

## Setup Instructions

### 1. Create virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## Data Ingestion

Run the ingestion pipeline:

```
python ingest.py
```

This will:

* Fetch Wikipedia articles
* Chunk text into smaller pieces
* Generate embeddings
* Store them in ChromaDB

---

## Run the API

Start FastAPI server:

```
uvicorn app:app --reload
```

Open in browser:

```
http://127.0.0.1:8000/docs
```

---

## Example Query

Use `/search` endpoint:

```
GET /search?q=What is a vector database?
```

Response:

* Top matching chunks
* Relevant context from ingested data

---

## Features

* 100% free and local (no paid APIs)
* Simple and extensible architecture
* Semantic search using embeddings
* Clean modular pipeline design

---

## Future Improvements

* Add LLM response generation (RAG completion)
* Add frontend UI (React / Next.js)
* Support multiple data sources (PDF, URLs)
* Add streaming responses

---

## Why this project?

This project showcases:

* Data pipeline design
* Vector databases & embeddings
* Backend API development
* Practical AI system implementation

---

## License

MIT License
