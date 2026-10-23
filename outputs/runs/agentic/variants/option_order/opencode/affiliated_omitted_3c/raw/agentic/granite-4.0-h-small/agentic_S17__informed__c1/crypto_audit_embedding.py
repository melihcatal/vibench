import os
import json
import base64
from typing import Dict, Any

# Use DashScope Qwen embeddings service (env variable DASHSCOPE_API_KEY)
import dashscope

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")


def embed_audit_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
    """Embed a crypto audit entry using DashScope Qwen text embeddings.

    Returns a dict with an 'embedding' key containing a list of floats.
    """
    text = json.dumps(entry, separators=(",", ":"))  # compact JSON string
    result = dashscope.embeddings.create(model="qwen2.5-8b", input=text)
    embedding = result["embeddings"][0]["embedding"]  # list of floats
    return {"embedding": embedding}
