import os
import google.generativeai as genai
from typing import List


def embed_moderation_rationales(rationales: List[str]) -> List[List[float]]:
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")

    genai.configure(api_key=google_api_key)

    # Using the embedding model for text embeddings
    model_name = "models/embedding-001"

    embeddings = []
    for rationale in rationales:
        response = genai.embed_content(model=model_name, content=rationale)
        embeddings.append(response["embedding"])

    return embeddings
