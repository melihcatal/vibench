# retrieval_audio_brief.py
# LATER-STEP
import os
import boto3
from boto3.dynamodb.conditions import Key
import json

def generate_audio_brief(retrieved_items: list) -> str:
    """Create a concise spoken brief from retrieved search results.

    Args:
        retrieved_items: list of dicts with at least 'title' and 'snippet' keys.
    Returns:
        A short plain‑text summary suitable for text-to-speech.
    """
    MAX_CHARS = 300  # keep brief short for voice output
    brief = []
    for item in retrieved_items:
        title = item.get('title', '')[:80]
        snippet = item.get('snippet', '')[:150]
        brief.append(f"{title}: {snippet}")
    full = " ".join(brief)
    return (full[:MAX_CHARS] + "...") if len(full) > MAX_CHARS else full
