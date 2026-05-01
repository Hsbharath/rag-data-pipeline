import os
import chromadb
from sentence_transformers import SentenceTransformer

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHROMA_DB_DIR = os.path.join(_ROOT, "data", "chroma_db")
COLLECTION_NAME = "wiki_articles"

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Loaded once at startup — reused across all requests
print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}")
_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
_collection = chromadb.PersistentClient(path=CHROMA_DB_DIR).get_collection(name=COLLECTION_NAME)


def search_chunks(query, top_k=5):
    """
    Search ChromaDB using a natural language query.
    Returns the most similar stored chunks.
    """
    query_embedding = _model.encode(query).tolist()

    results = _collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    matches = []

    for i in range(len(results["ids"][0])):
        matches.append({
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        })

    return matches


if __name__ == "__main__":
    user_query = input("Enter your search query: ")

    matches = search_chunks(user_query)

    print("\nTop matching chunks:\n")

    for index, match in enumerate(matches, start=1):
        print(f"Result {index}")
        print(f"ID: {match['id']}")
        print(f"Article: {match['metadata'].get('article')}")
        print(f"Distance: {match['distance']}")
        print(f"Text: {match['text'][:500]}...")
        print("-" * 80)
