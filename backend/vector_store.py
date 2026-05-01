import os
import json
import chromadb

EMBEDDINGS_DATA_DIR = "../data/embeddings"
CHROMA_DB_DIR = "../data/chroma_db"

COLLECTION_NAME = "wiki_articles"


def get_chroma_client():
    """
    Initialize ChromaDB client with local persistence.
    """
    return chromadb.PersistentClient(path=CHROMA_DB_DIR)


def get_or_create_collection(client):
    """
    Create collection if it doesn't exist.
    """
    return client.get_or_create_collection(name=COLLECTION_NAME)


def load_embedding_files():
    """
    Load all embedding JSON files from directory.
    """
    if not os.path.exists(EMBEDDINGS_DATA_DIR):
        raise FileNotFoundError(
            f"Embeddings directory not found: '{EMBEDDINGS_DATA_DIR}'\n"
            "Run embedder.py first to generate embeddings."
        )

    for filename in os.listdir(EMBEDDINGS_DATA_DIR):
        if not filename.endswith(".json"):
            continue

        file_path = os.path.join(EMBEDDINGS_DATA_DIR, filename)
        article_name = filename.replace("_chunks_embeddings.json", "").replace("_", " ")

        with open(file_path, "r", encoding="utf-8") as f:
            yield article_name, json.load(f)


def store_embeddings():
    """
    Main pipeline to store embeddings in ChromaDB.

    Steps:
    1. Initialize Chroma client
    2. Create/get collection
    3. Load embeddings
    4. Insert into vector DB
    """
    print("Connecting to ChromaDB...")
    client = get_chroma_client()

    collection = get_or_create_collection(client)

    total = 0

    for article_name, embedding_file in load_embedding_files():
        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for item in embedding_file:
            ids.append(item["id"])
            documents.append(item["text"])
            embeddings.append(item["embedding"])

            metadatas.append({
                "article": article_name
            })

        print(f"Inserting {len(ids)} records...")

        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

        total += len(ids)

    print(f"Stored total {total} embeddings in ChromaDB")


if __name__ == "__main__":
    store_embeddings()