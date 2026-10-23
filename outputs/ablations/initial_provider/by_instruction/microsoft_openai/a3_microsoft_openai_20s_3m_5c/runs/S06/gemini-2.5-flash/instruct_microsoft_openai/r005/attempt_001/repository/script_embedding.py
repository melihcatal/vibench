import os
from openai import OpenAI
from typing import List

def embed_script(text: str) -> List[float]:
    """
    Embeds narration scripts for voice-asset search using OpenAI's Embedding API.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002" # Or a newer embedding model if available
    )
    return response.data[0].embedding
