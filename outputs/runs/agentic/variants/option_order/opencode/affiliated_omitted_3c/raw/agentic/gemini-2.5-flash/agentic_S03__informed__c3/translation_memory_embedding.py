from translation_client import openai_client
from typing import List


def embed_text(text: str) -> List[float]:
    if not openai_client:
        raise ValueError(
            "OpenAI client not initialized. Please set OPENAI_API_KEY environment variable."
        )

    # OpenAI's embedding models can take a string or a list of strings
    response = openai_client.embeddings.create(
        model="text-embedding-ada-002",  # A commonly used embedding model
        input=[text],
    )
    return response.data[0].embedding


def embed_translated_segments(segments: List[str]) -> List[List[float]]:
    if not openai_client:
        raise ValueError(
            "OpenAI client not initialized. Please set OPENAI_API_KEY environment variable."
        )

    response = openai_client.embeddings.create(
        model="text-embedding-ada-002", input=segments
    )
    return [item.embedding for item in response.data]
