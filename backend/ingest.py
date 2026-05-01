import os
import wikipediaapi

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_DATA_DIR = os.path.join(_ROOT, "data", "raw")

# List of Wikipedia articles we want to ingest
# You can expand this later or even make it dynamic
ARTICLES = [
    "Artificial intelligence",
    "Machine learning",
    "Vector database",
    "Cloud computing",
    "Natural language processing",
]


def create_raw_data_folder():
    """
    Ensure the raw data folder exists before saving any files.
    'exist_ok=True' prevents errors if the folder is already created.
    """
    os.makedirs(RAW_DATA_DIR, exist_ok=True)


def get_wikipedia_page(title):
    """
    Fetch a Wikipedia page for a given title.

    We initialize the Wikipedia client here and request the page.
    If the page does not exist, we return None so the caller can skip it.
    """
    wiki = wikipediaapi.Wikipedia(
        user_agent="WikiVectorSearch/1.0",  # Required by Wikipedia API
        language="en"
    )

    page = wiki.page(title)

    # Handle case where page doesn't exist
    if not page.exists():
        print(f"Page not found: {title}")
        return None

    return page


def save_article(title, content):
    """
    Save the article text into a local file.

    We convert the title into a safe filename by:
    - making it lowercase
    - replacing spaces and slashes with underscores
    """
    safe_title = title.lower().replace(" ", "_").replace("/", "_")
    file_path = os.path.join(RAW_DATA_DIR, f"{safe_title}.txt")

    # Write the content to a .txt file using UTF-8 encoding
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"Saved: {file_path}")


def ingest_articles():
    """
    Main pipeline function.

    Steps:
    1. Ensure output folder exists
    2. Loop through each article
    3. Fetch content from Wikipedia
    4. Validate content
    5. Save to local files
    """
    create_raw_data_folder()

    for title in ARTICLES:
        try:
            print(f"Fetching: {title}")

            # Step 1: Fetch page
            page = get_wikipedia_page(title)

            # If page doesn't exist, skip to next article
            if page is None:
                continue

            # Step 2: Extract full text content
            content = page.text

            # Step 3: Validate content is not empty
            if not content.strip():
                print(f"No content found for: {title}")
                continue

            # Step 4: Save content locally
            save_article(title, content)

        except Exception as error:
            # Catch any unexpected error so one failure doesn't stop the pipeline
            print(f"Error fetching {title}: {error}")


# Entry point of the script
# This ensures the ingestion runs only when this file is executed directly
if __name__ == "__main__":
    ingest_articles()