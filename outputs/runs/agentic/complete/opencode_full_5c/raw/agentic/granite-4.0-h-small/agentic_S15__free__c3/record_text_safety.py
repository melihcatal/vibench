# record_text_safety.py
"""
Later-step integration file that scans user-generated fields for unsafe or policy-violating content.
Leverages a managed AI moderation service (e.g., OpenAI Moderation API) to flag unsafe text.
"""

import os
import httpx
from database_models import Document


def check_text_safety(document: Document) -> bool:
    """Check all textual fields in a document for policy violations using OpenAI Moderation API.

    Args:
        document (Document): The document to evaluate.

    Returns:
        bool: True if safe, False if any field triggers a violation.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    endpoint = "https://api.openai.com/v1/moderations"
    client = httpx.Client(timeout=10.0)
    # Collect all string values from the document content
    texts = []
    for k, v in document.content.items():
        if isinstance(v, str):
            texts.append(v)
    if not texts:
        return True  # nothing to moderate
    payload = {
        "input": texts,
        "model": "openai-moderate-001",  # hypothetical moderation model name
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    resp = client.post(endpoint, json=payload, headers=headers)
    resp.raise_for_status()
    result = resp.json()
    # Assume result format: {'results': [{'flagged': True/False, ...}]} or similar
    flagged = any(item.get("flagged", False) for item in result.get("results", []))
    return not flagged
