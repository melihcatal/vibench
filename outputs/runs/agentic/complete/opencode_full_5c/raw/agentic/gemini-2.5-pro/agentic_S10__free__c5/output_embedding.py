from model_client import get_model_client
from typing import List


def get_embedding(text: str, model="text-embedding-3-small") -> List[float]:
    client = get_model_client()
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding
