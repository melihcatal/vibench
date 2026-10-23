import os
from typing import List
from openai import OpenAI

from safety_client import get_openai_client
from safety_models import TextEmbedding

def embed_moderation_reason(reason_text: str) -> TextEmbedding:
    client = get_openai_client()

    # OpenAI's embedding API for generating vector representations of text
    response = client.embeddings.create(
        input=reason_text,
        model="text-embedding-3-small" # Concrete model identifier
    )

    embedding = response.data[0].embedding

    return TextEmbedding(
        text=reason_text,
        embedding=embedding
    )

def embed_multiple_reasons(reason_texts: List[str]) -> List[TextEmbedding]:
    client = get_openai_client()

    response = client.embeddings.create(
        input=reason_texts,
        model="text-embedding-3-small" # Concrete model identifier
    )

    embeddings = []
    for i, data_obj in enumerate(response.data):
        embeddings.append(
            TextEmbedding(
                text=reason_texts[i],
                embedding=data_obj.embedding
            )
        )
    return embeddings
