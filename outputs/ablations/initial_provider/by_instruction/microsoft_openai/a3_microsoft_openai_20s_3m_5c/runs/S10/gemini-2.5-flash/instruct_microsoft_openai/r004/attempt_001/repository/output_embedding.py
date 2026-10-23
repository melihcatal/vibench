import os
from openai import OpenAI
from typing import List

def get_embedding(text: str) -> List[float]:
    """
    Embeds model outputs for clustering or retrieval using OpenAI Embeddings.
    """
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    )

    response = client.embeddings.create(
        input=[text],
        model="text-embedding-3-small" # Using a concrete model identifier
    )
    return response.data[0].embedding