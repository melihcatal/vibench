import os
from typing import List, Union
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embed_single(model: str, text: str) -> List[float]:
    response = client.embeddings.create(model=model, input=text)
    return response.data[0].embedding


def embed_batch(model: str, texts: List[str]) -> List[List[float]]:
    response = client.embeddings.create(model=model, input=texts)
    return [data.embedding for data in response.data]
