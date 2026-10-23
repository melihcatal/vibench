import os
import google.generativeai as genai
from typing import List, Dict, Any


def embed_asset_metadata(metadata: Dict[str, Any], extracted_text: str) -> List[float]:
    """
    Creates an embedding for asset metadata and extracted text using Gemini API.

    Requires the GOOGLE_API_KEY environment variable to be set.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = "models/embedding-001"

    text_to_embed = f"Metadata: {str(metadata)}\nContent: {extracted_text}"

    embedding = genai.embed_content(model=model, content=text_to_embed)

    return embedding["embedding"]
