# Local helpers for request shaping, response parsing and normalization
import json
from typing import Any, Dict, Union

# Common request payloads that each hosted inference client expects


def build_chat_request(
    model: str, messages: list, max_tokens: int = 200
) -> Dict[str, Any]:
    """Create provider‑specific chat request dict.

    Args:
        model: Identifier for the hosted model.
        messages: List of {role, content} dicts (OpenAI style).
        max_tokens: Generation limit.

    Returns: Dict ready for the SDK call.
    """
    # Many SDKs (OpenAI, Amazon Bedrock, Google Gemini) accept the same shape.
    # Adjust if a specific provider requires a different top‑level key.
    request = {"model": model, "messages": messages, "max_tokens": max_tokens}
    # Example: IBM watsonx.ai expects 'inputs' instead of top‑level 'model'
    if model == "granite-4":
        request = {
            "inputs": {"prompt": "".join(m["content"] for m in messages)},
            "parameters": {"max_tokens": max_tokens},
        }
    return request


# Helper to safely parse possible JSON content from LLM output


def safe_json_parse(text: str) -> Union[Dict[str, Any], list, str]:
    """Attempt to decode JSON; fall back to raw string if decoding fails."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


# Normalization of provider‑specific response shapes to a unified internal format


def normalize_response(resp: Any) -> Dict[str, str]:
    """Convert any LLM response to {role: ..., content: ...}."""
    if isinstance(resp, dict):
        # OpenAI / Bedrock style
        choice = resp.get("choices", [{}])[0]
        return {
            "role": choice.get("role", "assistant"),
            "content": choice.get("message", {}).get("content", ""),
        }
    elif isinstance(resp, str):
        return {"role": "assistant", "content": resp}
    raise TypeError(f"Unexpected response type {type(resp)}")


# Example normalization usage (uncomment for quick check)
# client = get_text_chat_client('openai')
# raw = client(model='gpt-4o', messages=[{'role':'user','content':'hi'}], max_tokens=50)
# print(normalize_response(raw))
