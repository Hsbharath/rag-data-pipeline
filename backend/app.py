from fastapi import FastAPI, Query
from search import search_chunks
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="WikiVector Search API",
    description="Local semantic search API using ChromaDB and sentence-transformers",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "WikiVector Search API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/search")
def search(
    q: str = Query(..., description="Search query"),
    top_k: int = Query(5, description="Number of results to return")
):
    """
    Search stored Wikipedia chunks using natural language.
    """
    results = search_chunks(q, top_k)

    return {
        "query": q,
        "top_k": top_k,
        "results": results
    }