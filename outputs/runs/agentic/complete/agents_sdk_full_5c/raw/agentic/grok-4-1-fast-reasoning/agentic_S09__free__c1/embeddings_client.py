import os
from typing import List
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(
    text: str, 
    model: str = "text-embedding-3-small"
) -> List[float]:
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding

def get_embeddings(
    texts: List[str], 
    model: str = "text-embedding-3-small"
) -> List[List[float]]:
    response = client.embeddings.create(
        input=texts,
        model=model
    )
    return [item.embedding for item in response.data]
