import os
from model_models import normalize_response, NormalizedOutput
from model_client import ManagedModelClient

# Concrete provider for embeddings – OpenAI Embeddings (via Azure OpenAI endpoint as concrete service)
EMBED_PROVIDER: Literal["openai"] = "openai"

# Provider identifier used throughout the workflow
PROVIDER: Literal["huggingface"] = "huggingface"


def embed_output(raw_output: NormalizedOutput) -> list[float]:
    """Generate embeddings for provider output using the OpenAI Embeddings API.

    The concrete embedding service is identified by the EMBED_PROVIDER constant.
    """
    client = ManagedModelClient()
    text = raw_output["content"]
    # Simulated embedding call (replace with openai.OpenAI().embeddings.create)
    embedding_vector = _fake_embed(text)
    return embedding_vector


def _fake_embed(text: str) -> list[float]:
    # Placeholder: real implementation would return a list of floats
    return [0.1 * i for i in range(768)]  # 768‑dim embedding
