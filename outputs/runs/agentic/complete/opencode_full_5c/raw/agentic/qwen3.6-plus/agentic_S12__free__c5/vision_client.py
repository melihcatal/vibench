import os
import base64
from typing import Optional

from openai import OpenAI


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_VISION_MODEL = os.environ.get("OPENAI_VISION_MODEL", "gpt-4o-2024-11-20")
OPENAI_TIMEOUT = int(os.environ.get("OPENAI_TIMEOUT", "30"))


def get_openai_client() -> OpenAI:
    return OpenAI(
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
        timeout=OPENAI_TIMEOUT,
    )


def encode_image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as f:
        raw = f.read()
    encoded = base64.b64encode(raw).decode("utf-8")
    return encoded


def build_image_url(image_path: str) -> str:
    encoded = encode_image_to_base64(image_path)
    return f"data:image/jpeg;base64,{encoded}"


def build_vision_messages(
    system_prompt: str,
    user_prompt: str,
    image_url: str,
    detail: str = "auto",
) -> list[dict]:
    return [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": user_prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": image_url, "detail": detail},
                },
            ],
        },
    ]


def call_vision_api(
    messages: list[dict],
    model: Optional[str] = None,
    temperature: float = 0.0,
    max_tokens: int = 1024,
    response_format: Optional[dict] = None,
) -> str:
    client = get_openai_client()
    kwargs: dict = {
        "model": model or OPENAI_VISION_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if response_format is not None:
        kwargs["response_format"] = response_format
    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content or ""
