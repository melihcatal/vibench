import base64
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union
from urllib import request as urllib_request
from urllib.error import HTTPError, URLError


OPENAI_VISION_MODEL = os.environ.get("OPENAI_VISION_MODEL", "gpt-4o-mini")
OPENAI_API_URL = "https://api.openai.com/v1/responses"


def _load_image_bytes(image: Union[str, bytes, Path]) -> bytes:
    if isinstance(image, bytes):
        return image
    return Path(image).read_bytes()


def _to_data_url(image_bytes: bytes, mime_type: str = "image/png") -> str:
    return f"data:{mime_type};base64,{base64.b64encode(image_bytes).decode('ascii')}"


def extract_text(image: Union[str, bytes, Path], api_key: Optional[str] = None, mime_type: str = "image/png") -> str:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    payload: Dict[str, Any] = {
        "model": OPENAI_VISION_MODEL,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Extract all plain text from this scanned document image. Return only the text."},
                    {"type": "input_image", "image_url": _to_data_url(_load_image_bytes(image), mime_type)},
                ],
            }
        ],
    }

    req = urllib_request.Request(
        OPENAI_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib_request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"OpenAI API error: {exc.read().decode('utf-8', 'ignore')}") from exc
    except URLError as exc:
        raise RuntimeError(f"Network error: {exc.reason}") from exc

    output_text = data.get("output_text")
    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()

    texts = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"} and content.get("text"):
                texts.append(content["text"])
    return "\n".join(texts).strip()


__all__ = ["extract_text", "OPENAI_VISION_MODEL", "OPENAI_API_URL"]
