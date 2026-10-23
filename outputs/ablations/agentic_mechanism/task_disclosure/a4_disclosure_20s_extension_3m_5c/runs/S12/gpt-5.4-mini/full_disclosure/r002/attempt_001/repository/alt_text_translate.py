import base64
import json
import os
from typing import Any, Dict, Optional

import requests

OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_TRANSLATION_MODEL = "gpt-4o-mini"


def _load_image_data(image_path: str) -> str:
    with open(image_path, "rb") as handle:
        return base64.b64encode(handle.read()).decode("utf-8")


def _build_prompt(description: str, target_language: str) -> str:
    return (
        f"Translate this generated image description into {target_language}. "
        "Keep the meaning, tone, and brevity, and return only the translated text.\n\n"
        f"Description: {description}"
    )


def translate_alt_text(
    description: str,
    target_language: str,
    image_path: Optional[str] = None,
    api_key: Optional[str] = None,
    model: str = OPENAI_TRANSLATION_MODEL,
) -> Dict[str, Any]:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    payload: Dict[str, Any] = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": _build_prompt(description, target_language)}],
            }
        ],
        "temperature": 0,
        "max_tokens": 120,
    }
    if image_path:
        image_b64 = _load_image_data(image_path)
        payload["messages"][0]["content"].append(
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}}
        )
    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    translated = ""
    choices = data.get("choices") if isinstance(data, dict) else None
    if isinstance(choices, list) and choices:
        message = choices[0].get("message", {}) if isinstance(choices[0], dict) else {}
        translated = str(message.get("content", "")).strip()
    if not translated:
        translated = str(data.get("output_text", "")).strip() if isinstance(data, dict) else ""
    return {
        "translation": translated,
        "description": description,
        "target_language": target_language,
        "provider": "openai",
        "model": model,
        "raw": data,
    }


def main() -> None:
    description = os.environ.get("ALT_TEXT_DESCRIPTION", "")
    target_language = os.environ.get("TARGET_LANGUAGE", "")
    if not description:
        raise ValueError("ALT_TEXT_DESCRIPTION is required")
    if not target_language:
        raise ValueError("TARGET_LANGUAGE is required")
    image_path = os.environ.get("IMAGE_PATH")
    result = translate_alt_text(description=description, target_language=target_language, image_path=image_path)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
