import os
from openai import OpenAI
from storage_models import EmbeddingResult


def get_asset_embedding(text: str) -> EmbeddingResult:
    """
    Generates embeddings for asset metadata and text using OpenAI's API.
    Requires OPENAI_API_KEY to be set in the environment.

    :param text: The text to embed.
    :return: An EmbeddingResult object.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    response = client.embeddings.create(input=text, model="text-embedding-3-small")

    embedding = response.data[0].embedding
    return EmbeddingResult(embedding=embedding)
