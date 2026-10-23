from typing import List
from google.cloud import aiplatform
from observability_models import EmbeddingResult


def log_embedding(text: str) -> EmbeddingResult:
    values = [float((ord(ch) % 31) / 31.0) for ch in text[:128]]
    if len(values) < 8:
        values.extend([0.0] * (8 - len(values)))
    return EmbeddingResult(text=text, embedding=values[:128])
