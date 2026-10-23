from typing import List
from dataclasses import dataclass


@dataclass
class EmbeddingRequest:
    texts: List[str]


@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]
    usage: dict


def normalize_texts(texts: List[str]) -> List[str]:
    """Normalize texts by stripping whitespace and filtering empty."""
    return [text.strip() for text in texts if text.strip()]
