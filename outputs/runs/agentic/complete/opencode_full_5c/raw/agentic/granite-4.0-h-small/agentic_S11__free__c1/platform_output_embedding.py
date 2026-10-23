import json
from typing import Dict, Any
from model_models import ModelInvocationResponse

# Placeholder for an embedding service (e.g., OpenAI embeddings, Cohere, etc.)
# In a real implementation you would call the provider's embedding API or use a library.


def fake_embedding(text: str) -> str:
    # Returns a dummy embedding string; replace with actual vector generation
    return f"EMBED-{text[:10]}"


def platform_output_embedding(
    response: ModelInvocationResponse,
) -> ModelInvocationResponse:
    """Embeds model output for downstream evaluation or retrieval.

    Args:
        response: Original invocation response.

    Returns:
        Same response with an added `embedding` field in metadata.
    """
    # Embed only plain‑text outputs
    if not isinstance(response.output, str):
        embedding = None
    else:
        embedding = fake_embedding(response.output)
    updated_meta = response.metadata.copy()
    updated_meta["embedding"] = embedding
    return ModelInvocationResponse(
        output=response.output,
        metadata=updated_meta,
    )
