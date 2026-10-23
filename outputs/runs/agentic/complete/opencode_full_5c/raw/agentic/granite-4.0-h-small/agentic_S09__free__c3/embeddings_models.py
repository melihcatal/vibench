# embeddings_models.py
"""
["HELPER"] Request, response, and normalization helpers for Direct Embeddings API.
"""

from __future__ import annotations
from typing import List, TypedDict


class EmbedInputText(TypedDict):
    text: str


class EmbedRequest(TypedDict):
    texts: List[str]


class EmbedOutputEmbedding(TypedDict):
    vector: List[float]


class EmbedResponse(TypedDict):
    embeddings: List[EmbedOutputEmbedding]
