import json
import os
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROCESSED_DATA_DIR = os.path.join(_ROOT, "data", "processed")
EMBEDDINGS_DATA_DIR = os.path.join(_ROOT, "data", "embeddings")

# Free local embedding model
# It creates small, fast embeddings and works well for semantic search and clustering tasks.
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def create_embeddings_folder():
    """
    Create the embeddings folder if it doesn't exist.
    """
    if not os.path.exists(EMBEDDINGS_DATA_DIR):
        os.makedirs(EMBEDDINGS_DATA_DIR)

def load_embeddings_model():
    """
    Load the sentence-transformers model locally.
    The model may download once during the first run.
    After that, it will be cached and loaded from the local directory.
    """
    print(f"Loading embedding model '{EMBEDDING_MODEL_NAME}'...")
    return SentenceTransformer(EMBEDDING_MODEL_NAME)

def read_chunks(file_path):
    """
    Read the processed chunks from the JSON file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
    
def generate_embeddings(model, chunks):
    """
    Generate embeddings for each chunk of text.
    """
    print("Generating embeddings for chunks...")
    embedded_chunks = []
    for chunk in tqdm(chunks, desc="Genrating embeddings"):
        embedding = model.encode(chunk["text"], show_progress_bar=False)
        embedded_chunks.append({
            "id": chunk["chunk_id"],
            "text": chunk["text"],
            "embedding": embedding.tolist()  # Convert numpy array to list for JSON serialization
        })
    
    return embedded_chunks

def save_embeddings(article_name, embedded_chunks):
    """
    Save the generated embeddings to a JSON file.
    """
    output_path = os.path.join(EMBEDDINGS_DATA_DIR, f"{article_name}_embeddings.json")
    with open(os.path.join(EMBEDDINGS_DATA_DIR, f"{article_name}_embeddings.json"), "w") as f:
        json.dump(embedded_chunks, f, indent=2, ensure_ascii=False)
    
    print(f"Embeddings saved to {output_path}")

def process_embeddings():
    """
    Main function to process embeddings for all articles.

    Steps:
    1. Create the embeddings folder if it doesn't exist.
    2. Load the embedding model.
    3. For each article's chunks, generate embeddings and save them to a JSON file.
    4. Print progress and completion messages.
    5. Handle any exceptions that may occur during processing.
    """
    create_embeddings_folder()
    model = load_embeddings_model()

    for filename in os.listdir(PROCESSED_DATA_DIR):
        if not filename.endswith(".json"):
            continue

        file_path = os.path.join(PROCESSED_DATA_DIR, filename)
        article_name = filename.replace(".json", "")

        print(f"Processing chunks: {filename}")

        chunks = read_chunks(file_path)

        if not chunks:
            print(f"Skipping empty file: {filename}")
            continue

        embedded_chunks = generate_embeddings(model, chunks)
        save_embeddings(article_name, embedded_chunks)

if __name__ == "__main__":
    try:
        process_embeddings()
        print("All embeddings processed successfully.")
    except Exception as e:
        print(f"An error occurred during embedding processing: {e}")