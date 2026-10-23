# [HELPER] embeddings_models.py
# Define local request, response, and normalization helpers for Direct Embeddings API

# Provider: OpenAI Embeddings
# Integration signal: OPENAI_API_KEY environment variable

from typing import Dict, Any, List


def normalize_embedding_response(response: Dict[str, Any]) -> List[list[float]]:
    """Extract embedding vectors from OpenAI response."""
    return [item["embedding"] for item in response.get("data", [])]
