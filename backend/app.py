from fastapi import FastAPI, Query, HTTPException
from search import search_chunks
from rag import generate_answer
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
    top_k: int = Query(5, description="Number of results to return"),
    mode: str = Query("semantic", description="Search mode: 'semantic' or 'rag'"),
    detail: str = Query("high", description="RAG answer detail level: 'low' (~100 tokens) or 'high' (~500 tokens)")
):
    """
    Search stored Wikipedia chunks using natural language.

    mode=semantic (default): returns top matching chunks from ChromaDB.
    mode=rag: retrieves top chunks then generates a natural language answer.
    detail=low: concise answer. detail=high: detailed answer (only applies when mode=rag).
    """
    if mode not in ("semantic", "rag"):
        raise HTTPException(status_code=400, detail="mode must be 'semantic' or 'rag'")
    if detail not in ("low", "high"):
        raise HTTPException(status_code=400, detail="detail must be 'low' or 'high'")

    chunks = search_chunks(q, top_k)

    if mode == "rag":
        answer = generate_answer(q, chunks, detail=detail)
        return {
            "query": q,
            "top_k": top_k,
            "mode": "rag",
            "detail": detail,
            "answer": answer,
            "source_chunks": chunks,
        }

    return {
        "query": q,
        "top_k": top_k,
        "mode": "semantic",
        "results": chunks,
    }