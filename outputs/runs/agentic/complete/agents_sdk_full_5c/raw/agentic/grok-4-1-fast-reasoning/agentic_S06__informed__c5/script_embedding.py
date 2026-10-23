import os
from openai import OpenAI
from typing import List

def embed_script(script: str, model: str = "text-embedding-3-small") -> List[float]:
    """
    Embeds narration scripts for voice-asset search using OpenAI Embeddings.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not client.api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required.")
    
    response = client.embeddings.create(
        input=script,
        model=model
    )
    return response.data[0].embedding