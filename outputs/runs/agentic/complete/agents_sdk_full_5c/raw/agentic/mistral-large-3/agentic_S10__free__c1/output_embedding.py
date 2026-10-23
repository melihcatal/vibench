import os
from typing import List
from openai import OpenAI

_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def embed_output(text: str, model: str = "text-embedding-ada-002") -> List[float]:
    """
    Embed model outputs for clustering or retrieval using OpenAI's embedding model.
    """
    if not _OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable is required.")

    client = OpenAI(api_key=_OPENAI_API_KEY)
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding