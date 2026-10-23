from typing import Dict, List
from openai import OpenAI
import os


def moderation_reason_embedding(reason: str) -> List[float]:
    """Embed moderation rationales for case retrieval using OpenAI Embeddings API."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(input=reason, model="text-embedding-3-small")
    return response.data[0].embedding
