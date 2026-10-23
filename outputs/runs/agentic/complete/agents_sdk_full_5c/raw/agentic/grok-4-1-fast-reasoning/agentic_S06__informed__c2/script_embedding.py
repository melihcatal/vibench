import os
from openai import OpenAI

def embed_script(script: str) -> list[float]:
    """
    Embeds narration scripts for voice-asset search using OpenAI embeddings.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=script,
    )
    return response.data[0].embedding
