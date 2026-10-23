import os
from openai import OpenAI
from typing import List


def get_platform_output_embedding(output: str) -> List[float]:
    """
    Generates embedding for platform output using OpenAI Embeddings API.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not client.api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=output,
    )
    return list(response.data[0].embedding)
