import os
from openai import OpenAI
from typing import List


def get_script_embedding(text: str) -> List[float]:
    """
    Generates an embedding for a narration script using OpenAI's API.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    response = client.embeddings.create(input=text, model="text-embedding-3-small")

    return response.data[0].embedding
