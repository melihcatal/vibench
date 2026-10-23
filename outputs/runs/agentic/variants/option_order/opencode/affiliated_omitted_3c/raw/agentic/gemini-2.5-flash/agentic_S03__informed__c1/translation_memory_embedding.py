import os
from openai import OpenAI
from typing import List


def embed_segment(segment: str) -> List[float]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    response = client.embeddings.create(
        input=[segment],
        model="text-embedding-ada-002",  # Using a concrete model identifier
    )
    return response.data[0].embedding
