import json
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_DATA_DIR = os.path.join(_ROOT, "data", "raw")
PROCRESSED_DATA_DIR = os.path.join(_ROOT, "data", "processed")

# Chuck settings            
# chunk_size: max number of characters in each chunk
# chunk_overlap: characters repeated between chunks to keep context
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

def create_processed_data_folder():
    """Ensure the processed data directory exists."""
    if not os.path.exists(PROCRESSED_DATA_DIR):
        os.makedirs(PROCRESSED_DATA_DIR)

def read_raw_articles(file_path):
    """Read the raw article text from a file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
    

def split_text_into_chunks(text):
    """
    Read the raw article text and split it into chunks using Langchain's RecursiveCharacterTextSplitter.
    RecursiveCharacterTextSplitter will split the text into chunks of a specified size, with some overlap to maintain context.

    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return splitter.split_text(text)

def save_chucks(article_name, chunks):
    """
    Save the list of chunks to a JSON file in the processed directory.

    Each chunk has:
    - article_name: the name of the original article
    - chunk_id: a unique identifier for the chunk (e.g., "article_name_chunk_1")
    - text: the chunk of text itself
    """
    output_file = os.path.join(PROCRESSED_DATA_DIR, f"{article_name}_chunks.json")
    
    chunk_records = []
    for i, chunk in enumerate(chunks):
        chunk_id = f"{article_name}_chunk_{i+1}"
        chunk_records.append({
            "article_name": article_name,
            "chunk_id": chunk_id,
            "text": chunk
        })

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(chunk_records, file, ensure_ascii=False, indent=2)

    print(f"Saved chunks to: {output_file}")


def process_articles():

    """
        Main chuncking pipeline
        Steps:
        1. Ensure processed data folder exists
        2. Loop through each raw article file
        3. Read content and split into chunks
        4. Save chunks to processed directory as JSON
    """
    create_processed_data_folder()

    for filename in os.listdir(RAW_DATA_DIR):
        
        if filename.startswith("."):
            continue  # Skip hidden files

        if not filename.endswith(".txt"):
            print(f"Skipping non-text file: {filename}")
            continue

        if filename.endswith(".txt"):
            file_path = os.path.join(RAW_DATA_DIR, filename)
            article_name = filename.replace(".txt", "")
            print(f"Processing: {article_name}")
            text = read_raw_articles(file_path)

            if not text.strip():
                print(f"No content found in: {filename}")
                continue

            chunks = split_text_into_chunks(text)
            save_chucks(article_name, chunks)
            print(f"Processed and saved chunks for: {filename}")

if __name__ == "__main__":
    process_articles()