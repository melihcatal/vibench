from __future__ import annotations

from typing import List

from openai import OpenAI

from storage_models import ObjectMetadata


def embed_object_metadata_and_text(metadata: ObjectMetadata, extracted_text: str, model: str = "text-embedding-3-large") -> List[float]:
    client = OpenAI()
    payload = f"bucket={metadata.bucket}\nname={metadata.name}\ncontent_type={metadata.content_type}\nsize={metadata.size}\nmetadata={metadata.metadata}\ntext={extracted_text}"
    response = client.embeddings.create(model=model, input=payload)
    return list(response.data[0].embedding)
