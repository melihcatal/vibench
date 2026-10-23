import os
from openai import OpenAI
from typing import List

from safety_client import get_openai_client
from safety_models import EmbeddingInput, EmbeddingOutput

def embed_moderation_reason(embedding_input: EmbeddingInput) -> EmbeddingOutput:
    client = get_openai_client()

    try:
        response = client.embeddings.create(
            input=embedding_input.text,
            model="text-embedding-3-small"  # Concrete model identifier
        )
        
        embedding = response.data[0].embedding
        return EmbeddingOutput(embedding=embedding)
    except Exception as e:
        print(f"Error generating embedding with OpenAI: {e}")
        return EmbeddingOutput(embedding=[])
