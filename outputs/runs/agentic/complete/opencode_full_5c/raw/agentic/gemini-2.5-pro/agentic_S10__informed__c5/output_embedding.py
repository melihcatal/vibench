import os
from dotenv import load_dotenv
import cohere
from typing import List

load_dotenv()


def embed_outputs_cohere(texts: List[str]) -> List[List[float]]:
    """
    Embeds model outputs for clustering or retrieval using Cohere.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY not found in environment variables.")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=texts, model="embed-english-v3.0", input_type="search_document"
    )
    return response.embeddings
