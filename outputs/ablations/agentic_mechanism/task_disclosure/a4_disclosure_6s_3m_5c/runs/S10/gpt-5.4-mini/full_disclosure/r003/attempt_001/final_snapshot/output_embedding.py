import os
from typing import List

from openai import OpenAI


def embed_outputs(outputs: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(model=model, input=outputs)
    return [item.embedding for item in response.data]
