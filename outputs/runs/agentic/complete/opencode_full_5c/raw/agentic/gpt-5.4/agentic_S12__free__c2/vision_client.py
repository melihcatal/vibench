from __future__ import annotations

import base64
import json
import mimetypes
import os
from typing import Any, Dict

import requests

from vision_models import ImageInput


GOOGLE_VISION_API_URL = "https://vision.googleapis.com/v1/images:annotate"
OPENAI_RESPONSES_API_URL = "https://api.openai.com/v1/responses"


def _read_image_bytes(image: ImageInput) -> bytes:
    if image.image_path:
        with open(image.image_path, "rb") as handle:
            return handle.read()
    raise ValueError("image_path is required for local image processing")


def resolve_mime_type(image: ImageInput) -> str:
    if image.mime_type:
        return image.mime_type
    if image.image_path:
        guessed, _ = mimetypes.guess_type(image.image_path)
        if guessed:
            return guessed
    return "image/jpeg"


def build_google_image(image: ImageInput) -> Dict[str, Any]:
    if image.image_url:
        return {"source": {"imageUri": image.image_url}}
    content = base64.b64encode(_read_image_bytes(image)).decode("utf-8")
    return {"content": content}


def google_vision_annotate(
    feature_type: str, image: ImageInput, max_results: int = 10
) -> Dict[str, Any]:
    api_key = os.environ["GOOGLE_CLOUD_API_KEY"]
    payload = {
        "requests": [
            {
                "image": build_google_image(image),
                "features": [{"type": feature_type, "maxResults": max_results}],
            }
        ]
    }
    response = requests.post(
        f"{GOOGLE_VISION_API_URL}?key={api_key}",
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["responses"][0]


def openai_visual_response(
    prompt: str, image: ImageInput, model: str = "gpt-4.1-mini"
) -> Dict[str, Any]:
    api_key = os.environ["OPENAI_API_KEY"]
    if image.image_url:
        image_part: Dict[str, Any] = {
            "type": "input_image",
            "image_url": image.image_url,
        }
    else:
        b64 = base64.b64encode(_read_image_bytes(image)).decode("utf-8")
        mime_type = resolve_mime_type(image)
        image_part = {
            "type": "input_image",
            "image_url": f"data:{mime_type};base64,{b64}",
        }
    payload = {
        "model": model,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    image_part,
                ],
            }
        ],
    }
    response = requests.post(
        OPENAI_RESPONSES_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps(payload),
        timeout=60,
    )
    response.raise_for_status()
    return response.json()
