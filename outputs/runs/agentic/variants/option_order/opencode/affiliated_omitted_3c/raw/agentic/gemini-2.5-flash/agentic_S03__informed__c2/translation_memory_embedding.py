import os
from openai import OpenAI
from translation_models import EmbeddingRequest
import dataclasses
from typing import List


@dataclasses.dataclass
class EmbeddingResponse:
    embedding: List[float]


def embed_translation_segment(request: EmbeddingRequest) -> EmbeddingResponse:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")

    client = OpenAI(api_key=api_key)

    response = client.embeddings.create(
        input=[request.text],
        model="text-embedding-ada-002",  # Using a concrete model ID from OpenAI
    )

    if response.data:
        return EmbeddingResponse(embedding=response.data[0].embedding)
    else:
        return EmbeddingResponse(embedding=[])
