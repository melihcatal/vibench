import os
from openai import OpenAI
from typing import List


def get_text_embeddings(
    texts: List[str], model="text-embedding-3-small"
) -> List[List[float]]:
    """
    Generates embeddings for a list of texts using OpenAI API.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    texts = [text.replace("\n", " ") for text in texts]

    response = client.embeddings.create(input=texts, model=model)

    return [embedding.embedding for embedding in response.data]
