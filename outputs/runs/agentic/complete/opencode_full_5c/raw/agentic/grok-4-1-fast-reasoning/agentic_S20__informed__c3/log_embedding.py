import os
from openai import OpenAI
from typing import List


def log_embedding(message: str) -> List[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model="text-embedding-3-small", input=message)
    return response.data[0].embedding
