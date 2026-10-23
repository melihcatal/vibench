from __future__ import annotations

import base64
import json
import mimetypes
import os
from typing import Any, Dict, Optional

from anthropic import Anthropic
from deepl import Translator
from google.cloud import storage
from google.cloud import vision
from openai import OpenAI

from vision_models import ImageSource


OPENAI_VISION_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini")
OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")
ANTHROPIC_SUMMARY_MODEL = os.getenv("ANTHROPIC_SUMMARY_MODEL", "claude-3-5-sonnet-20241022")
DEEPL_TARGET_LANG = os.getenv("DEEPL_TARGET_LANG", "ES")
GCS_ARCHIVE_BUCKET = os.getenv("GCS_ARCHIVE_BUCKET", "")


def get_google_vision_client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_anthropic_client() -> Anthropic:
    return Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def get_deepl_client() -> Translator:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    return Translator(auth_key)


def get_storage_client() -> storage.Client:
    return storage.Client()


def load_image_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as infile:
        return infile.read()


def build_vision_image(source: ImageSource) -> vision.Image:
    if source.image_path:
        return vision.Image(content=load_image_bytes(source.image_path))
    if source.image_url:
        return vision.Image(source=vision.ImageSource(image_uri=source.image_url))
    raise ValueError("Either image_path or image_url must be provided")


def build_openai_image_input(source: ImageSource) -> Dict[str, Any]:
    if source.image_url:
        return {"type": "input_image", "image_url": source.image_url}
    if source.image_path:
        image_bytes = load_image_bytes(source.image_path)
        mime_type = mimetypes.guess_type(source.image_path)[0] or "image/jpeg"
        encoded = base64.b64encode(image_bytes).decode("utf-8")
        return {"type": "input_image", "image_url": f"data:{mime_type};base64,{encoded}"}
    raise ValueError("Either image_path or image_url must be provided")


def dump_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2, default=str)
