from __future__ import annotations

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"



def platform_output_embedding(text: str) -> dict:
    client = OpenAI()
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=text,
    )
    item = response.data[0]
    return {
        "model": OPENAI_EMBEDDING_MODEL,
        "embedding": item.embedding,
        "dimensions": len(item.embedding),
        "provider_response": response,
    }
