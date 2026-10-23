from typing import Literal

# Provider identifier - set to the service you chose in embeddings_client.py
EMBEDDING_PROVIDER: Literal[
    "openai", "bedrock", "gemini", "cohere", "dashscope", "watsonx"
] = "openai"  # <-- replace with actual provider name

# Request/response type aliases (examples)
EmbeddingRequest = list[str]
EmbeddingResponse = list[list[float]]
EmbeddingResult = tuple[int, float]

# Normalization helpers


def normalize_text(text: str) -> str:
    """Basic text cleaning before embedding."""
    return text.strip().lower()


def validate_response(response: EmbeddingResponse) -> bool:
    """Validate shape of embedding response."""
    return isinstance(response, list) and all(isinstance(v, list) for v in response)
