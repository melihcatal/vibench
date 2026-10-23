import os
import openai
from typing import List


def embed_transcript(segments: List[str]) -> List[str]:
    """Create embeddings for each transcript segment using OpenAI's embedding API.

    Args:
        segments: List of text chunks from a transcript.

    Returns:
        List of embedding vectors (as strings) corresponding to each segment.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY environment variable")

    embeddings = []
    for seg in segments:
        resp = openai.Embedding.create(
            input=seg,
            model="text-embedding-ada-002",
        )
        # The returned embedding is a list of floats; join to a compact string
        vec = resp["data"][0]["embedding"]
        embeddings.append(" ".join(map(str, vec)))
    return embeddings
