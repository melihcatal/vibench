from __future__ import annotations

from openai import OpenAI


def asset_metadata_embedding(
    metadata: dict, extracted_text: str, model: str = "text-embedding-3-small"
) -> list[float]:
    client = OpenAI()
    payload = f"metadata={metadata}\ntext={extracted_text}"
    response = client.embeddings.create(model=model, input=payload)
    return response.data[0].embedding
