from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Optional

import requests


OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_VISION_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4.1-mini")


@dataclass(frozen=True)
class VisionConfig:
    api_key: str
    api_base: str = OPENAI_API_BASE
    model: str = OPENAI_VISION_MODEL
    timeout: float = 60.0


def load_config() -> VisionConfig:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return VisionConfig(
        api_key=api_key,
        api_base=os.getenv("OPENAI_API_BASE", OPENAI_API_BASE),
        model=os.getenv("OPENAI_VISION_MODEL", OPENAI_VISION_MODEL),
        timeout=float(os.getenv("OPENAI_TIMEOUT", "60")),
    )


@lru_cache(maxsize=1)
def get_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    return session


def image_to_data_url(image_path: str | Path) -> str:
    path = Path(image_path)
    ext = path.suffix.lower().lstrip(".") or "png"
    mime = "jpeg" if ext in {"jpg", "jpeg"} else ext
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/{mime};base64,{data}"


def build_vision_payload(prompt: str, image_path: str | Path, *, model: Optional[str] = None, max_output_tokens: int = 300) -> Dict[str, Any]:
    config = load_config()
    return {
        "model": model or config.model,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": image_to_data_url(image_path)},
                ],
            }
        ],
        "max_output_tokens": max_output_tokens,
    }


def call_vision(prompt: str, image_path: str | Path, *, model: Optional[str] = None, max_output_tokens: int = 300) -> str:
    config = load_config()
    payload = build_vision_payload(prompt, image_path, model=model, max_output_tokens=max_output_tokens)
    response = get_session().post(
        f"{config.api_base.rstrip('/')}/responses",
        headers={"Authorization": f"Bearer {config.api_key}"},
        json=payload,
        timeout=config.timeout,
    )
    response.raise_for_status()
    data = response.json()
    output = data.get("output", [])
    texts = []
    for item in output:
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"} and content.get("text"):
                texts.append(content["text"])
    if texts:
        return "\n".join(texts).strip()
    return ""
