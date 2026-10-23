import json
from typing import TypedDict, List


# Request model for retrieving a secret
class GetSecretRequest(TypedDict):
    secret_id: str
    version_id: str | None


# Response model for a successful secret retrieval
class GetSecretSuccessResponse(TypedDict):
    secret_id: str
    version_id: str
    payload: dict


# Normalized response type used across implementations
class NormalizedSecretResponse(TypedDict):
    provider: str
    secret_id: str
    version_id: str
    payload: dict


def normalize_secret_response(provider: str, raw: dict) -> NormalizedSecretResponse:
    """Normalize provider-specific secret payload into a consistent shape."""
    return {
        "provider": provider,
        "secret_id": raw.get("secret_id"),
        "version_id": raw.get("version_id"),
        "payload": raw.get("payload", {}),
    }


if __name__ == "__main__":
    # Example usage with the IBM client (already defined elsewhere in this repo)
    from fetch_api_key import fetch_api_key

    raw = {
        "secret_id": "api-key-secret",
        "version_id": "latest",
        "payload": {"api_key": "abcd1234"},
    }
    print("Normalized:", normalize_secret_response("ibm", raw))
