import os
from typing import List

import dashscope
from dashscope import TextEmbedding


def embed_output(
    texts: List[str],
    model_id: str = "text-embedding-v1",
) -> List[List[float]]:
    """
    Embed model outputs for clustering or retrieval using DashScope Embeddings.
    """
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set")

    dashscope.api_key = api_key

    responses = TextEmbedding.call(
        model=model_id,
        input=texts,
    )

    if responses.status_code != 200:
        raise RuntimeError(f"Embedding request failed: {responses.message}")

    return [embedding["embedding"] for embedding in responses.output["embeddings"]]
