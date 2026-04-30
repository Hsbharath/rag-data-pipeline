import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_DB_DIR = "../data/chroma_db"
COLLECTION_NAME = "wiki_articles"

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_embedding_model():
    """
    Load the same embedding model used during PR5.
    Query embeddings must use the same model as stored chunk embeddings.
    """
    print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}")
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


def get_collection():
    """
    Connect to local ChromaDB and load the existing collection.
    """
    client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    return client.get_collection(name=COLLECTION_NAME)


def search_chunks(query, top_k=5):
    """
    Search ChromaDB using a natural language query.
    Returns the most similar stored chunks.
    """
    model = load_embedding_model()
    collection = get_collection()

    query_embedding = model.encode(query).tolist()

    results = collection.query(
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