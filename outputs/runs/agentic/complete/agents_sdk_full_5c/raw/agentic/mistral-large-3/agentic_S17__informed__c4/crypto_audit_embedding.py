import os
from openai import OpenAI
from typing import List


def generate_crypto_audit_embedding(text: str) -> List[float]:
    """
    Generates embeddings for crypto audit notes using OpenAI Embeddings.
    """
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding