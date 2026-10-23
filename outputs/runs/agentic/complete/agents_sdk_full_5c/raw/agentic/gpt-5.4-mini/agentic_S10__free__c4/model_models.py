from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


@dataclass
class LLMRequest:
    prompt: str
    context: str | None = None
    model: str | None = None


@dataclass
class LLMResponse:
    text: str
    raw: Any | None = None


def normalize_text_response(response: Any) -> str:
    if hasattr(response, "output_text") and getattr(response, "output_text"):
        return response.output_text
    try:
        return response.output[0].content[0].text
    except Exception:
        return str(response)


def normalize_json_response(response: Any) -> dict[str, Any]:
    if hasattr(response, "output_text") and getattr(response, "output_text"):
        return json.loads(response.output_text)
    try:
        text = response.output[0].content[0].text
        return json.loads(text)
    except Exception as exc:
        raise ValueError("Unable to normalize JSON response") from exc


def extract_embedding_vector(response: Any) -> list[float]:
    data = getattr(response, "data", None)
    if data:
        return list(data[0].embedding)
    raise ValueError("Unable to normalize embedding response")
