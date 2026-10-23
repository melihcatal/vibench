# [HELPER] embeddings_models.py
# Define local request, response, and normalization helpers for Direct Embeddings API

from typing import List, Tuple

# Request payload structure for embedding creation (OpenAI style)
EmbedRequest = dict[str, str | List[str]]
# Response data element structure (single embedding)
EmbedResponseItem = dict[str, list[float]]

# Simple normalization to ensure embeddings are lists of floats
_TOP_N = 10


def normalize_embedding(embedding: list[float]) -> list[float]:
    """Ensure embedding length is at most _TOP_N dimensions."""
    if len(embedding) > _TOP_N:
        return embedding[:_TOP_N]
    return embedding


# Batch helper that normalizes each embedding in a list


def batch_normalize(embeddings: List[list[float]]) -> List[list[float]]:
    return [normalize_embedding(e) for e in embeddings]


# Example of parsing a raw OpenAI response into a list of normalized embeddings
def parse_openai_response(resp: dict) -> List[list[float]]:
    """Extract and normalize embeddings from an OpenAI Embedding.create response."""
    return batch_normalize([item["embedding"] for item in resp["data"]])
