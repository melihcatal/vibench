import os
from openai import OpenAI
from embeddings_client import EMBEDDING_MODEL
from typing import List

def embed_text(text: str) -> List[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=text,
        model=EMBEDDING_MODEL
    )
    return response.data[0].embedding