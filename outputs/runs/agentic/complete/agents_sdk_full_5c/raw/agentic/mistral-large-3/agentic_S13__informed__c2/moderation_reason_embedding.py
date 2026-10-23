"""
Embed moderation rationales for case retrieval using OpenAI Embeddings.
"""
import os
from typing import List, Dict

from openai import OpenAI


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embed_moderation_reason(text: str) -> List[float]:
    """Embed moderation rationale using OpenAI."""
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding