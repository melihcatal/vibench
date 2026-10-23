import os
from typing import List
from openai import OpenAI


def ocr_embedding(sections: List[str]) -> List[List[float]]:
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(input=sections, model="text-embedding-3-small")
    return [embedding.embedding for embedding in response.data]
