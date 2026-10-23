# retrieval_audio_brief.py
import os
import openai
from typing import List

def generate_audio_brief(retrieved: List[tuple[str, float]],
                          max_words: int = 50) -> str:
    """Create a concise spoken brief from a list of (document, score) pairs.

    Args:
        retrieved (List[tuple[str, float]]): output from semantic search.
        max_words (int): approximate word limit for the brief.
    
    Returns:
        str: brief text ready for TTS conversion.
    """
    # Summarize top matching documents
    brief_parts = []
    for i, (doc, score) in enumerate(retrieved, start=1):
        snippet = doc.strip()[:max_words]
        if len(doc) > max_words:
            snippet += "..."  # ellipsis for brevity
        brief_parts.append(f"Result {i}: {snippet} (confidence {score:.3f})")
    return "\\n".join(brief_parts)
