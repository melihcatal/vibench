import os
from typing import List
import openai


def create_translation_embedding(text: str) -> List[float]:
    """
    Creates an embedding for a text segment using OpenAI.

    Requires OPENAI_API_KEY environment variable.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY environment variable not set.")

    client = openai.OpenAI(api_key=api_key)

    response = client.embeddings.create(input=text, model="text-embedding-ada-002")
    return response.data[0].embedding
