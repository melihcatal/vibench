from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from speech_models import EmbeddingVector, normalize_transcript_text


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"



def embed_caption_chunks(chunks: Iterable[str]) -> List[EmbeddingVector]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    cleaned_chunks = [normalize_transcript_text(chunk) for chunk in chunks if normalize_transcript_text(chunk)]
    if not cleaned_chunks:
        return []
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=cleaned_chunks)
    return [
        EmbeddingVector(text=text, vector=item.embedding, model=OPENAI_EMBEDDING_MODEL)
        for text, item in zip(cleaned_chunks, response.data)
    ]
