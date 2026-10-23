import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
DEFAULT_OCR_MODEL = os.getenv("OPENAI_OCR_MODEL", os.getenv("OPENAI_MODEL", "gpt-5.4-mini"))
DEFAULT_LAYOUT_MODEL = os.getenv("OPENAI_LAYOUT_MODEL", os.getenv("OPENAI_MODEL", "gpt-5.4-mini"))
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"


@dataclass(frozen=True)
class OCRConfig:
    api_key: Optional[str] = None
    model: str = DEFAULT_OCR_MODEL
    timeout: int = 120
    base_url: str = OPENAI_RESPONSES_URL


@dataclass(frozen=True)
class LayoutConfig:
    api_key: Optional[str] = None
    model: str = DEFAULT_LAYOUT_MODEL
    timeout: int = 120
    base_url: str = OPENAI_RESPONSES_URL


def get_api_key(api_key: Optional[str] = None) -> str:
    key = api_key or os.getenv(OPENAI_API_KEY_ENV)
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return key


def build_headers(api_key: Optional[str] = None) -> Dict[str, str]:
    key = get_api_key(api_key)
    return {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}


def build_responses_payload(model: str, prompt: str, response_format: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "model": model,
        "input": [{"role": "user", "content": [{"type": "input_text", "text": prompt}]}],
    }
    if response_format is not None:
        payload["response_format"] = response_format
    return payload


def post_json(url: str, payload: Dict[str, Any], api_key: Optional[str] = None, timeout: int = 120) -> Dict[str, Any]:
    response = requests.post(url, headers=build_headers(api_key), json=payload, timeout=timeout)
    response.raise_for_status()
    return response.json()


def extract_output_text(response_json: Dict[str, Any]) -> str:
    text_parts = []
    for item in response_json.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text_parts.append(content.get("text", ""))
    if text_parts:
        return "".join(text_parts).strip()
    if isinstance(response_json.get("output_text"), str):
        return response_json["output_text"].strip()
    return ""


def ocr_config(api_key: Optional[str] = None, model: Optional[str] = None, timeout: int = 120, base_url: Optional[str] = None) -> OCRConfig:
    return OCRConfig(api_key=api_key, model=model or DEFAULT_OCR_MODEL, timeout=timeout, base_url=base_url or OPENAI_RESPONSES_URL)


def layout_config(api_key: Optional[str] = None, model: Optional[str] = None, timeout: int = 120, base_url: Optional[str] = None) -> LayoutConfig:
    return LayoutConfig(api_key=api_key, model=model or DEFAULT_LAYOUT_MODEL, timeout=timeout, base_url=base_url or OPENAI_RESPONSES_URL)
