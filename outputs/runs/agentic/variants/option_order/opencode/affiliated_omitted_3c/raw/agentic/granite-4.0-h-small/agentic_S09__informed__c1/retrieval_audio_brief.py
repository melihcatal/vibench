import os
from embeddings_client import get_embedder
from embeddings_models import normalize_embedding
from similarity_score import cosine_similarity
import random


def generate_audio_brief(retrieved_docs: list, max_length: int = 150) -> str:
    """Produce a spoken summary from retrieved documents.

    Args:
        retrieved_docs (list): List of document texts returned by search.
        max_length (int): Desired spoken summary length in characters.

    Returns:
        str: Brief textual summary suitable for text-to-speech.
    """
    # Simple heuristic: concatenate titles or first sentences, then truncate
    if not retrieved_docs:
        return "No documents retrieved."
    # Placeholder: pick the first doc for brevity
    brief = retrieved_docs[0][:max_length]
    # Ensure it ends at a sentence boundary if possible
    if "\n" in brief:
        brief = brief[: brief.rfind("\n")]
    return brief.strip()
