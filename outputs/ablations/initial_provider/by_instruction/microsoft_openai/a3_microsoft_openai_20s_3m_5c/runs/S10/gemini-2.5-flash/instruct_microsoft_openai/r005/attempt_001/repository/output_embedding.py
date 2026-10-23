import os
from openai import OpenAI
from typing import List

def embed_output(text: str) -> List[float]:
    """
    Embeds model outputs for clustering or retrieval using OpenAI Embeddings.
    """
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        organization=os.environ.get("OPENAI_ORGANIZATION"),
    )

    response = client.embeddings.create(
        input=[text],
        model="text-embedding-ada-002"  # Or another suitable OpenAI embedding model
    )
    return response.data[0].embedding
