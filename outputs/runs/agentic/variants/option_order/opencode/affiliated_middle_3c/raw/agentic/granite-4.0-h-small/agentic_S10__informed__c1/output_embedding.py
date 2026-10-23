import os
import dashscope

# Example: DashScope text embeddings (Direct Embeddings API)\n# Provider identification via import name and model ID

# ------------------------------------------------------------------\n# Configuration – set env var before running\n# ------------------------------------------------------------------\nDASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
if not DASHSCOPE_API_KEY:
    raise RuntimeError("Set DASHSCOPE_API_KEY environment variable.")


def embed_text(text: str, model: str = "text-embedding-ada-002") -> list[float]:
    """Generates an embedding vector for the input text using DashScope's embedding endpoint."""
    # DashScope provides a simple SDK call; the model ID is explicit
    response = dashscope.embeddings.create(
        model=model,
        text=text,
    )
    # Expected response: {"embeddings": [{"embedding": [0.1, 0.2, ...]}]}
    embedding_vector = response.embeddings[0]["embedding"]
    return embedding_vector
