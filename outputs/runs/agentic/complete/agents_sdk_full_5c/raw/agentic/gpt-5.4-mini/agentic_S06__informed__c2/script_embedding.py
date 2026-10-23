from __future__ import annotations

from typing import List

from google import genai

from speech_models import EmbeddingResult, normalize_text

GEMINI_EMBEDDING_MODEL = "text-embedding-004"


def embed_script(text: str) -> EmbeddingResult:
    client = genai.Client()
    response = client.models.embed_content(model=GEMINI_EMBEDDING_MODEL, contents=normalize_text(text))
    vector: List[float] = list(response.embeddings[0].values)
    return EmbeddingResult(text=text, provider="Gemini embeddings", vector=vector, metadata={"model": GEMINI_EMBEDDING_MODEL})
