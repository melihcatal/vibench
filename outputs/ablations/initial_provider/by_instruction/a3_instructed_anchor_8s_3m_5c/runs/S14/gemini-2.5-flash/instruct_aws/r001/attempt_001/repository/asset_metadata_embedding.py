import os
import google.generativeai as genai
from typing import List

def embed_asset_metadata(text: str) -> List[float]:
    """Embeds object metadata and extracted text for search using Google Cloud Generative AI (embedding-001).

    Args:
        text: The combined text of object metadata and extracted content to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    # Ensure GOOGLE_API_KEY environment variable is set for authentication
    # os.environ['GOOGLE_API_KEY'] = "YOUR_API_KEY"

    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('embedding-001') # Using embedding-001 for embeddings

    response = model.embed_content(content=text, task_type="RETRIEVAL_DOCUMENT")
    return response['embedding']
