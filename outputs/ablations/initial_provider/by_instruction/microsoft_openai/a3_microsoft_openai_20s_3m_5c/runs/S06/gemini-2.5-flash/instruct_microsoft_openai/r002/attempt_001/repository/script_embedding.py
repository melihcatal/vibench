from openai import OpenAI
import os
from typing import List

def embed_script(text: str) -> List[float]:
    """
    Embeds narration scripts for voice-asset search using OpenAI Embeddings API.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002" # Or another suitable embedding model
    )
    return response.data[0].embedding
