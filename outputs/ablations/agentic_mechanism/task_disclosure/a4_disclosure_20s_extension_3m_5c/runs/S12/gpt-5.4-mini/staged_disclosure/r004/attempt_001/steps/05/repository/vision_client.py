import base64
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib import request


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
OPENAI_DEFAULT_VISION_MODEL = "gpt-4.1-mini"


@dataclass(frozen=True)
class VisionClientConfig:
    api_key: str
    model: str = OPENAI_DEFAULT_VISION_MODEL


def load_vision_config() -> VisionClientConfig:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    model = os.environ.get("OPENAI_VISION_MODEL", OPENAI_DEFAULT_VISION_MODEL)
    return VisionClientConfig(api_key=api_key, model=model)


def _read_image_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()


def _image_data_url(image_bytes: bytes, mime_type: str = "image/jpeg") -> str:
    return f"data:{mime_type};base64,{base64.b64encode(image_bytes).decode('ascii')}"


def _extract_text(result: Dict[str, Any]) -> str:
    text_parts = []
    for item in result.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"} and content.get("text"):
                text_parts.append(content["text"])
    return "\n".join(text_parts).strip()


def _post_openai_responses(payload: Dict[str, Any], api_key: str) -> Dict[str, Any]:
    req = request.Request(
        OPENAI_RESPONSES_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def static_image_prompt(image_path: str, prompt: str, model: Optional[str] = None, mime_type: str = "image/jpeg") -> str:
    config = load_vision_config()
    image_bytes = _read_image_bytes(image_path)
    payload = {
        "model": model or config.model,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": _image_data_url(image_bytes, mime_type=mime_type)},
                ],
            }
        ],
    }
    return _extract_text(_post_openai_responses(payload, config.api_key))


def visual_understanding(image_path: str, question: str, model: Optional[str] = None, mime_type: str = "image/jpeg") -> str:
    config = load_vision_config()
    image_bytes = _read_image_bytes(image_path)
    payload = {
        "model": model or config.model,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": question},
                    {"type": "input_image", "image_url": _image_data_url(image_bytes, mime_type=mime_type)},
                ],
            }
        ],
    }
    return _extract_text(_post_openai_responses(payload, config.api_key))
