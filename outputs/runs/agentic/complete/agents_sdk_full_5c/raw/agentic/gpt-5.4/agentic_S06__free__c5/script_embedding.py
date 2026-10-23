from __future__ import annotations

import os

import google.generativeai as genai

from speech_models import EmbeddingResult


DEFAULT_EMBEDDING_MODEL = "models/text-embedding-004"


def embed_script(text: str, model: str = DEFAULT_EMBEDDING_MODEL) -> EmbeddingResult:
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY or GOOGLE_API_KEY is required")
    genai.configure(api_key=api_key)
    response = genai.embed_content(
        model=model,
        content=text,
        task_type="RETRIEVAL_DOCUMENT",
    )
    return EmbeddingResult(vector=list(response["embedding"]), model="text-embedding-004")
