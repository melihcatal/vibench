# transcript_embedding.py
import os
from typing import Dict, Any, List

# Use DashScope embeddings API to embed transcript segments for semantic retrieval
from dashscope import embeddings  # type: ignore

# Load configuration from environment variables
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")


def transcript_embedding(
    transcript_segments: List[str], model_id: str = "dashscope/embeddings/text"
) -> Dict[str, Any]:
    """Creates embeddings for each transcript segment.

    Uses the DashScope Embeddings API as the concrete provider.
    Returns a dictionary mapping segment indices to embedding vectors (as lists of floats).
    """
    client = embeddings.Client(api_key=DASHSCOPE_API_KEY)
    # Batch the inputs; DashScope accepts up to 1000 tokens per request
    responses = client.embeddings(texts=transcript_segments, model=model_id)
    # Normalize response into a simple dict
    result = {str(i): resp["embedding"] for i, resp in enumerate(responses)}
    return result
