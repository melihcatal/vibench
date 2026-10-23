import os
from typing import List
from openai import OpenAI

def log_embedding(messages: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    embeddings = []
    for message in messages:
        response = client.embeddings.create(
            input=message,
            model=model
        )
        embeddings.append(response.data[0].embedding)
    return embeddings
