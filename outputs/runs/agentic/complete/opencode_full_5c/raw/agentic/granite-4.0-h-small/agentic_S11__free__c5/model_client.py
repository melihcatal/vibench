# model_client.py
# [HELPER]
# Local configuration and client helper utilities for Managed Model Platform Workflow

import os
from typing import Literal

# Concrete provider selection (example: OpenAI)
PROVIDER_NAME: Literal["openai"] = "openai"

# Load API key from environment or a local placeholder file
API_KEY = os.getenv("OPENAI_API_KEY", "/run/secrets/openai-api-key")


# ---------------------------------------------------------------------------
# Client factory - returns a provider‑specific client instance
# ---------------------------------------------------------------------------
class ManagedModelClient:
    """Thin wrapper around the concrete provider SDK."""

    def __init__(self, provider: Literal["openai"] = "openai"):
        self.provider = provider
        if provider == "openai":
            from openai import OpenAI  # type: ignore

            self._client = OpenAI(api_key=API_KEY)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def invoke(self, request) -> dict:
        # Assuming request is compatible with OpenAI's ChatCompletion API
        return self._client.chat.completions.create(**request.to_dict())

    def resolve_resource(self, request) -> dict:
        # Dummy placeholder – real implementation would call provider resource APIs
        return {"resource_id": request.name, "status": "available"}

    def stream(self, request) -> dict:
        # Placeholder – real streaming client would be async and preserve provider objects
        return {"stream_id": request.deployment_id, "status": "streaming"}

    def get_metadata(self, request) -> dict:
        # Placeholder – real call would fetch usage, run details, etc.
        return {
            "run_id": request.run_id,
            "usage": {"tokens": 123, "prompt_tokens": 60, "completion_tokens": 63},
        }


# ---------------------------------------------------------------------------
# Helper utilities for converting between our local model_models objects and
# the concrete provider SDK payloads
# ---------------------------------------------------------------------------


def to_provider_payload(obj) -> dict:
    """Serialize a local model_models object to a dict consumable by the provider SDK."""
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    return obj


def from_provider_payload(data: dict, cls) -> object:
    """Deserialize provider SDK response into our local response class."""
    # Simple example – assume cls has a from_dict classmethod
    return cls.from_dict(data)


# ---------------------------------------------------------------------------
# Example usage (uncomment to test locally)
# ---------------------------------------------------------------------------
# if __name__ == "__main__":
#     client = ManagedModelClient()
#     resp = client.invoke({"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "Hello"}]})
#     print(resp)
