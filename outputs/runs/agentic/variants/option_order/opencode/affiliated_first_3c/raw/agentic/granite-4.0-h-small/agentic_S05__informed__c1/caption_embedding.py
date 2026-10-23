"""
Embed caption chunks for semantic meeting search using IBM Slate embeddings.
Uses SDK: ibm-watsonx-ai (or REST). Returns embeddings as numpy arrays.
Credentials: WATSONX_API_KEY, WATSONX_PROJECT_ID
"""

import os
import asyncio
from ibm_watsonx_ai import Client
from ibm_watsonx_ai.embeddings import EmbeddingsModelOptions, EmbeddingsModelSettings
import numpy as np

EMBEDDING_MODEL = "embedding-001"  # watsonx.ai slate embedding model id


async def embed_chunk(chunk: str) -> np.ndarray:
    """Returns embedding vector for a single caption chunk."""
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    client = Client(
        base_url="https://api.watsonx.ai", api_key=api_key, project_id=project_id
    )
    options = EmbeddingsModelOptions(model_id=EMBEDDING_MODEL, texts=[chunk])
    response = client.embeddings.create_embed(args=options)
    # Response shape depends on model; usually returns list of vectors
    vectors = response["results"][0]["embeddings"]
    # Normalize to numpy array and ensure shape (vector_dim,)
    return np.array(vectors)


async def embed_all(source: Iterator[str]) -> list[np.ndarray]:
    """Embeds all caption chunks sequentially."""
    embeddings = []
    async for txt in source:
        vec = await embed_chunk(txt)
        embeddings.append(vec)
    return embeddings


def demo_source() -> Iterator[str]:
    for i in range(3):
        yield f"Demo chunk {i}. This is useful for meeting retrieval."


if __name__ == "__main__":
    results = asyncio.run(embed_all(demo_source()))
    for i, vec in enumerate(results):
        print(f"Embedding {i} shape: {vec.shape}")
