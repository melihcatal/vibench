import os
from embeddings_client import DirectEmbeddingsConfig
from embeddings_models import EmbeddingsModels

# Configuration
config = DirectEmbeddingsConfig(
    service="DashScope",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="text-embedding-ada-002",
)


def summarize_embedding_job(results: dict) -> str:
    """Summarize the results of an embedding job.",

    Args:
        results (dict): Raw output from the embedding job, may include timings,
                        dimensions, and success flags.

    Returns:
        str: Human‑readable summary.",
    """
    # Example: extract useful fields
    dims = results.get("dimensions", "unknown")
    time_ms = results.get("time_ms", "unknown")
    status = "SUCCESS" if results.get("success", False) else "FAILURE"
    return f"Embedding job completed in {time_ms}ms, dimensions {dims}, status {status}"
