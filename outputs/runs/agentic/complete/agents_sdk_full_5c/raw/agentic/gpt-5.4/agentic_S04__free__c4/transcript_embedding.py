from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from speech_models import EmbeddingVector

OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


def transcript_embedding(segments: Iterable[str]) -> List[dict]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=list(segments))
    results: List[dict] = []
    for item, source_text in zip(response.data, list(segments)):
        embedding = EmbeddingVector(text=source_text, vector=item.embedding, model=OPENAI_EMBEDDING_MODEL)
        results.append(embedding.__dict__)
    return results
