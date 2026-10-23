import os
from typing import List
from openai import OpenAI
from translation_models import EmbeddingResult

def embed_text_for_translation_memory(text: str, model: str = "text-embedding-3-small") -> EmbeddingResult:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    response = client.embeddings.create(
        input=text,
        model=model,
    )

    embedding = response.data[0].embedding
    return EmbeddingResult(embedding=embedding, model=model)
