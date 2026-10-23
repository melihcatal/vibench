from __future__ import annotations

import os
from typing import Mapping, Sequence

from openai import OpenAI

from storage_models import EmbeddingResult



def embed_asset_metadata(metadata: Mapping[str, object], extracted_text: str, tags: Sequence[str] | None = None) -> EmbeddingResult:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    tag_text = ", ".join(tags or ())
    serialized = "\n".join(
        [
            "Asset metadata embedding payload:",
            *(f"{key}: {value}" for key, value in metadata.items()),
            f"tags: {tag_text}",
            f"extracted_text: {extracted_text}",
        ]
    )
    response = client.embeddings.create(model=model, input=serialized)
    vector = response.data[0].embedding
    return EmbeddingResult(vector=vector, model=model, dimensions=len(vector))
