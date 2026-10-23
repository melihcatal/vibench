import os
from openai import OpenAI
from typing import List

def embed_platform_output(text: str, model: str = "text-embedding-3-small") -> List[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding
