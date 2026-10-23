import base64
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI


@dataclass
class VisionConfig:
    model: str
    api_key: Optional[str]


def load_vision_config(default_model: str) -> VisionConfig:
    return VisionConfig(model=os.getenv("OPENAI_VISION_MODEL", default_model), api_key=os.getenv("OPENAI_API_KEY"))


def build_openai_client(api_key: Optional[str] = None) -> OpenAI:
    return OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))


def image_url_from_path(image_path: str) -> str:
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    ext = os.path.splitext(image_path)[1].lower().lstrip(".") or "png"
    mime = "jpeg" if ext in {"jpg", "jpeg"} else ext
    return f"data:image/{mime};base64,{encoded}"


def chat_vision_completion(client: OpenAI, model: str, prompt: str, image_path: str, max_tokens: int = 300) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url_from_path(image_path)}},
                ],
            }
        ],
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content or ""


def chat_text_completion(client: OpenAI, model: str, prompt: str, max_tokens: int = 300) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content or ""


def normalize_text_response(text: str) -> str:
    return " ".join(text.strip().split())
