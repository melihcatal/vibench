from openai import OpenAI
import os
from typing import List

def embed_script(script: str, model_id: str = "text-embedding-3-small") -> List[float]:
    """
    Embed narration script using OpenAI Embeddings API.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        input=script,
        model=model_id
    )
    return response.data[0].embedding
