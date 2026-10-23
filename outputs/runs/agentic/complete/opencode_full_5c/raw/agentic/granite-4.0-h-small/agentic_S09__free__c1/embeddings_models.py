# [HELPER] embeddings_models.py
# Local request, response, and normalization helpers for Direct Embeddings API

from typing import List, TypedDict


# Request model for embeddings API
class EmbedRequest(TypedDict):
    model: str
    input: str | List[str]


# Response model for a single embedding response
class EmbedResponseSingle(TypedDict):
    embedding: List[float]


# Response model for batch embedding responses
class EmbedBatchResponse(TypedDict):
    data: List[EmbedResponseSingle]


# Normalized embedding response used internally
EmbedResponse = TypedDict(
    "EmbedResponse",
    {
        "embedding": List[float],
        "model": str,
    },
)

EmbedBatchResponse = TypedDict(
    "EmbedBatchResponse",
    {
        "embeddings": List[List[float]],
        "model": str,
    },
)
