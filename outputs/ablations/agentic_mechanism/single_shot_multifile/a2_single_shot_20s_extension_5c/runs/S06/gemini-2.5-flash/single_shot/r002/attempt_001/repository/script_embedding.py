import os
from openai import OpenAI
from typing import List

def get_script_embedding(
    text: str,
    model: str = "text-embedding-3-small"
) -> List[float]:
    """
    Generates an embedding for the narration script using OpenAI Embeddings.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    response = client.embeddings.create(
        input=[text],
        model=model
    )

    if response.data:
        return response.data[0].embedding
    return []
