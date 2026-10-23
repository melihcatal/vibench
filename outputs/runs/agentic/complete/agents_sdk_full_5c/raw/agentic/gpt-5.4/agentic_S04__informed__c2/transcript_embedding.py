from __future__ import annotations

import os
from typing import Dict, List, Sequence

from openai import OpenAI

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def transcript_embedding(segments: Sequence[Dict[str, str]]) -> List[Dict[str, object]]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    texts = [segment.get("text", "") for segment in segments]
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=texts)
    embedded: List[Dict[str, object]] = []
    for segment, item in zip(segments, response.data):
        enriched = dict(segment)
        enriched["embedding_model"] = OPENAI_EMBEDDING_MODEL
        enriched["embedding"] = item.embedding
        embedded.append(enriched)
    return embedded
