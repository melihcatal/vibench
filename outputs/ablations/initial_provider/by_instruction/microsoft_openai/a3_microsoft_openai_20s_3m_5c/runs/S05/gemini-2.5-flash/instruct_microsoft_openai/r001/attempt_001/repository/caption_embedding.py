import os
import cohere
from dotenv import load_dotenv
from typing import List

load_dotenv() # Load environment variables from .env file

# Cohere API Key from environment variable
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY environment variable not set.")

co = cohere.Client(COHERE_API_KEY)

def embed_caption_chunks(caption_chunks: List[str], model: str = "embed-english-v3.0", input_type: str = "search_document") -> List[List[float]]:
    """
    Embeds caption chunks for semantic meeting search using Cohere Embed API.
    """
    if not caption_chunks:
        return []

    print(f"Embedding {len(caption_chunks)} caption chunks using Cohere {model}...")
    try:
        response = co.embed(
            texts=caption_chunks,
            model=model,
            input_type=input_type
        )
        return response.embeddings
    except Exception as e:
        print(f"Error embedding with Cohere: {e}")
        return []

if __name__ == "__main__":
    # This is a placeholder for receiving live caption chunks.
    dummy_caption_chunks = [
        "The discussion revolved around the new product features and their impact on user experience.",
        "Financial projections for the next quarter indicate a steady growth in revenue.",
        "Action items include updating the documentation and scheduling a follow-up with the development team.",
        "The marketing team presented their strategy for the upcoming campaign.",
        "Customer feedback was largely positive, but some areas for improvement were identified."
    ]

    print("Starting caption embedding simulation...")
    embeddings = embed_caption_chunks(dummy_caption_chunks)

    if embeddings:
        print(f"Generated {len(embeddings)} embeddings. First embedding snippet: {embeddings[0][:5]}...")
        # In a real application, these embeddings would be stored in a vector database
        # for semantic search or similarity comparison.
    else:
        print("No embeddings generated.")
