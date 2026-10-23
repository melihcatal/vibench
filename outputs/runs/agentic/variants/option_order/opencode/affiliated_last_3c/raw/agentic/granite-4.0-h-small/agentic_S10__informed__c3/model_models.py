from __future__ import annotations
import json
from typing import Any, Dict, Union

Response = Dict[str, Any]

# ---------------------------------------------------------------------------
# Request helpers
# ---------------------------------------------------------------------------


def build_chat_request(
    prompt: str, temperature: float = 0.2, max_tokens: int = 256
) -> Dict[str, Any]:
    """
    Constructs a request payload for the hosted LLM inference endpoint.
    The shape mirrors the Anthropic /v1/messages API, but the concrete
    provider can be swapped simply by changing the import path.
    """
    return {
        "model": "claude-3-5-sonnet-20240620",  # concrete model identifier
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }


# ---------------------------------------------------------------------------
# Response helpers
# ---------------------------------------------------------------------------


def parse_completion(response: Response) -> str:
    """
    Extracts the raw completion text from the provider response.
    Normalizes different providers (Anthropic, OpenAI, etc.) to a
    simple string output.
    """
    # Anthropic response shape example:
    # {"completion": "..."}
    return response.get("completion", "")


# ---------------------------------------------------------------------------
# Normalization utilities
# ---------------------------------------------------------------------------


def normalize_response(raw: Union[str, Dict[str, Any]]) -> str:
    """
    Normalizes varied output formats (raw string vs structured JSON) to a
    consistent string representation suitable for downstream processing.
    """
    if isinstance(raw, str):
        return raw.strip()
    # If the raw result is already a dict (e.g., extracted JSON)
    return json.dumps(raw, ensure_ascii=False)
