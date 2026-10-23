import os
import json
import requests
from observability_models import LogEntry
from typing import List, Dict

SLATE_EMBEDDING_ENDPOINT = "https://api.watsonx.ai/v1/models/embed-slate-300-en/embed"
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

SAFE_THRESHOLD = 0.0  # placeholder for safety; embedded regardless

def embed_log_message(text: str) -> List[float]:
    """Embed selected log message for semantic retrieval using IBM Slate embeddings.

    Args:
        text: Log message to embed.
    Returns:
        List of float embedding vectors.
    """
    if not WATSONX_API_KEY or not WATSONX_PROJECT_ID:
        raise RuntimeError("Missing WATSONX_API_KEY or WATSONX_PROJECT_ID environment variables")
    payload = {
        "input": {
            "text": text
        }
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {WATSONX_API_KEY}"
    }
    response = requests.post(SLATE_EMBEDDING_ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()
    # Expected response shape: {"embeddings": [[float,...], ...]}
    embeddings = response.json().get("embeddings", [])
    if not embeddings:
        raise ValueError("Empty embedding response")
    return embeddings[0]   # one vector per message


def batch_embed_log_messages(messages: List[str]) -> List[List[float]]:
    """Embed a batch of log messages, returning a list of embedding vectors.

    Args:
        messages: List of log message strings.
    Returns:
        List of embedding vectors, same order as input.
    """
    payload = {
        "input": {
            "text": messages
        }
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {WATSONX_API_KEY}"
    }
    response = requests.post(SLATE_EMBEDDING_ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()
    embeddings = response.json().get("embeddings", [])
    if not embeddings:
        raise ValueError("Empty embedding response")
    return embeddings
