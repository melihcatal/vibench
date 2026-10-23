import base64
import mimetypes
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
DEFAULT_VISION_MODEL = "gpt-4.1-mini"


@dataclass
class VisionClientConfig:
    api_key: str
    model: str = DEFAULT_VISION_MODEL
    timeout: float = 60.0


def load_config() -> VisionClientConfig:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    model = os.getenv("OPENAI_VISION_MODEL", DEFAULT_VISION_MODEL).strip() or DEFAULT_VISION_MODEL
    timeout = float(os.getenv("OPENAI_VISION_TIMEOUT", "60"))
    return VisionClientConfig(api_key=api_key, model=model, timeout=timeout)


def _guess_mime_type(path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(str(path))
    if mime_type:
        return mime_type
    return "application/octet-stream"


def image_file_to_data_url(image_path: str) -> str:
    path = Path(image_path)
    data = path.read_bytes()
    mime_type = _guess_mime_type(path)
    encoded = base64.b64encode(data).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def build_static_image_payload(image_path: str, prompt: str = "Describe this image.") -> List[Dict[str, Any]]:
    return [
        {"type": "input_text", "text": prompt},
        {"type": "input_image", "image_url": image_file_to_data_url(image_path)},
    ]


def build_visual_understanding_payload(image_path: str, prompt: str) -> List[Dict[str, Any]]:
    return build_static_image_payload(image_path=image_path, prompt=prompt)


def _extract_output_text(response_json: Dict[str, Any]) -> str:
    texts: List[str] = []
    for item in response_json.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text = content.get("text")
                if text:
                    texts.append(text)
    if texts:
        return "\n".join(texts)
    return response_json.get("output_text", "") or ""


def analyze_image(image_path: str, prompt: str = "Describe this image.", config: Optional[VisionClientConfig] = None) -> str:
    cfg = config or load_config()
    payload = {
        "model": cfg.model,
        "input": [
            {
                "role": "user",
                "content": build_static_image_payload(image_path, prompt),
            }
        ],
    }
    headers = {
        "Authorization": f"Bearer {cfg.api_key}",
        "Content-Type": "application/json",
    }
    response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=cfg.timeout)
    response.raise_for_status()
    return _extract_output_text(response.json())


def get_local_vision_config() -> Dict[str, Any]:
    cfg = load_config()
    return {"provider": "openai", "api_url": OPENAI_API_URL, "model": cfg.model, "timeout": cfg.timeout}
