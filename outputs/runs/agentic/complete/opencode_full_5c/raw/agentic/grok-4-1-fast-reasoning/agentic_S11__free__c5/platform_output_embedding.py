import os
from openai import OpenAI
from typing import List


def platform_output_embedding(content: str) -> List[float]:
    """
    Embeds platform output using provider embedding model.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY must be set")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        input=content,
        model="text-embedding-3-small",
    )
    return [float(x) for x in response.data[0].embedding]
