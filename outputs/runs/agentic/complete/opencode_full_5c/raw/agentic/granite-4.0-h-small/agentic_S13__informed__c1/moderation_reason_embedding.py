import os
import requests
from safety_models import create_request, parse_response

API_KEY = os.getenv("PERSPECTIVE_API_KEY")

EMBEDDING_ENDPOINT = "https://some-embedding-service/embed"  # placeholder


def moderation_reason_embedding(reason_text: str) -> dict:
    """Embed moderation rationales for case retrieval.
    Returns dict with embedding vector.
    """
    if not API_KEY:
        raise RuntimeError("Set PERSPECTIVE_API_KEY environment variable")
    payload = {"text": reason_text}
    resp = requests.post(EMBEDDING_ENDPOINT, json=payload)
    resp.raise_for_status()
    return resp.json()  # expected to contain vector field
