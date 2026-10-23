import os
from openai import OpenAI
from typing import List

def platform_output_embedding(text: str) -> List[float]:
    """
    Generate embedding for platform output using OpenAI Embeddings API.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding
