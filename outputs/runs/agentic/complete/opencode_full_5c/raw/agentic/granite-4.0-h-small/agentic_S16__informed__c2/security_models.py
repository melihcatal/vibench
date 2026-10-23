import json
from typing import TypedDict

# Local models for request/response normalization
RequestPayload = TypedDict(
    "RequestPayload",
    {
        "secret_name": str,
        "optional_params": dict,
    },
)
ResponsePayload = TypedDict(
    "ResponsePayload",
    {
        "value": str,
        "metadata": dict,
    },
)

# Helper to validate secret metadata (e.g., unsafe text in labels)
UNSAFE_PATTERNS = [r"admin", r"password", r"key"]


def security_check(secret_metadata: dict) -> bool:
    for pattern in UNSAFE_PATTERNS:
        if any(
            re.search(pattern, str(v), re.IGNORECASE) for v in secret_metadata.values()
        ):
            return False
    return True


# Example normalizer for embedding secret notes after safety check


def normalize_for_embedding(secret_name: str, metadata: dict, content: str) -> dict:
    if not security_check(metadata):
        raise ValueError("Unsafe text detected in secret metadata")
    return {
        "secret_name": secret_name,
        "content_embeddings": content,  # placeholder for embedding vector
        "labels": metadata.get("labels", []),
    }
