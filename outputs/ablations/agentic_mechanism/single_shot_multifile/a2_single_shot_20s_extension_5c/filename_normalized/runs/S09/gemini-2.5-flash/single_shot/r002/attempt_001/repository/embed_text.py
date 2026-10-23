import os
from typing import List

from openai import OpenAI

def embed_text(text: str) -> List[float]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding