from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


DEFAULT_OCR_HOST = os.getenv("OCR_API_HOST", "https://vision.googleapis.com")
DEFAULT_LAYOUT_HOST = os.getenv("LAYOUT_API_HOST", "https://documentai.googleapis.com")


@dataclass(frozen=True)
class OCRClientConfig:
    api_key: str
    host: str = DEFAULT_OCR_HOST
    timeout: float = 60.0


@dataclass(frozen=True)
class LayoutClientConfig:
    api_key: str
    host: str = DEFAULT_LAYOUT_HOST
    timeout: float = 60.0


def _normalize_host(host: str) -> str:
    return host.rstrip("/")


def load_ocr_config(api_key: Optional[str] = None, host: Optional[str] = None, timeout: Optional[float] = None) -> OCRClientConfig:
    key = api_key or os.getenv("GOOGLE_CLOUD_API_KEY") or os.getenv("OCR_API_KEY")
    if not key:
        raise ValueError("Missing OCR API key")
    return OCRClientConfig(api_key=key, host=_normalize_host(host or DEFAULT_OCR_HOST), timeout=timeout or 60.0)


def load_layout_config(api_key: Optional[str] = None, host: Optional[str] = None, timeout: Optional[float] = None) -> LayoutClientConfig:
    key = api_key or os.getenv("GOOGLE_CLOUD_API_KEY") or os.getenv("LAYOUT_API_KEY")
    if not key:
        raise ValueError("Missing layout API key")
    return LayoutClientConfig(api_key=key, host=_normalize_host(host or DEFAULT_LAYOUT_HOST), timeout=timeout or 60.0)


class OCRClient:
    def __init__(self, config: OCRClientConfig):
        self.config = config
        self.session = requests.Session()

    def detect_text(self, image_bytes: bytes, mime_type: str = "image/png") -> Dict[str, Any]:
        url = f"{self.config.host}/v1/images:annotate"
        payload = {
            "requests": [
                {
                    "image": {"content": image_bytes.decode("latin1")},
                    "features": [{"type": "TEXT_DETECTION"}],
                    "imageContext": {"languageHints": ["en"]},
                }
            ]
        }
        headers = {"Content-Type": "application/json", "X-API-Key": self.config.api_key}
        response = self.session.post(url, json=payload, headers=headers, timeout=self.config.timeout)
        response.raise_for_status()
        return response.json()


class LayoutClient:
    def __init__(self, config: LayoutClientConfig):
        self.config = config
        self.session = requests.Session()

    def process_document(self, raw_document: bytes, content_type: str = "application/pdf") -> Dict[str, Any]:
        url = f"{self.config.host}/v1beta3/projects/-/locations/us/processors/ocr:process"
        headers = {
            "Content-Type": content_type,
            "X-API-Key": self.config.api_key,
        }
        response = self.session.post(url, data=raw_document, headers=headers, timeout=self.config.timeout)
        response.raise_for_status()
        return response.json()


def create_ocr_client(api_key: Optional[str] = None, host: Optional[str] = None, timeout: Optional[float] = None) -> OCRClient:
    return OCRClient(load_ocr_config(api_key=api_key, host=host, timeout=timeout))


def create_layout_client(api_key: Optional[str] = None, host: Optional[str] = None, timeout: Optional[float] = None) -> LayoutClient:
    return LayoutClient(load_layout_config(api_key=api_key, host=host, timeout=timeout))
