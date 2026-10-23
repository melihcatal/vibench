import json
from dataclasses import dataclass
from typing import Any


@dataclass
class TextRequest:
    prompt: str
    model: str | None = None


@dataclass
class TextResponse:
    text: str
    raw: Any = None


@dataclass
class JsonResponse:
    data: dict
    raw: Any = None


def normalize_text_result(response: Any) -> str:
    output = getattr(response, "output_text", None)
    if output:
        return output
    try:
        return response.output[0].content[0].text
    except Exception:
        return str(response)


def normalize_json_result(response: Any) -> dict:
    text = normalize_text_result(response)
    return json.loads(text)
