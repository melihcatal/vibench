import re
from embeddings_client import get_embeddings_client

_BLOCKLIST = [
    r"\bpassword\b",
    r"\bssn\b",
    r"\bcredit\s*card\b",
    r"\bapi\s*key\b",
]


def corpus_safety(text: str) -> dict:
    lowered = text.lower()
    matches = [pattern for pattern in _BLOCKLIST if re.search(pattern, lowered)]
    client = get_embeddings_client()
    model_name = "text-embedding-3-small"
    _ = client.embeddings.create(model=model_name, input=text[:2000])
    return {
        "safe": not matches,
        "matches": matches,
        "provider": "openai",
        "model": model_name,
    }
