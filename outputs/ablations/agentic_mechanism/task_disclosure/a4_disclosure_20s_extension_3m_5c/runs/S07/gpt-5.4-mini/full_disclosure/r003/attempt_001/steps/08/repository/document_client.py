from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


DEFAULT_OCR_BASE_URL = "https://api.assemblyai.com/v2"
DEFAULT_LAYOUT_BASE_URL = "https://api.assemblyai.com/v2"


@dataclass(frozen=True)
class OCRConfig:
    api_key: Optional[str] = None
    base_url: str = DEFAULT_OCR_BASE_URL
    timeout: float = 60.0

    @classmethod
    def from_env(cls) -> "OCRConfig":
        return cls(
            api_key=os.getenv("ASSEMBLYAI_API_KEY"),
            base_url=os.getenv("OCR_API_BASE_URL", DEFAULT_OCR_BASE_URL),
            timeout=float(os.getenv("OCR_API_TIMEOUT", "60")),
        )


@dataclass(frozen=True)
class LayoutExtractionConfig:
    api_key: Optional[str] = None
    base_url: str = DEFAULT_LAYOUT_BASE_URL
    timeout: float = 60.0

    @classmethod
    def from_env(cls) -> "LayoutExtractionConfig":
        return cls(
            api_key=os.getenv("ASSEMBLYAI_API_KEY"),
            base_url=os.getenv("LAYOUT_API_BASE_URL", DEFAULT_LAYOUT_BASE_URL),
            timeout=float(os.getenv("LAYOUT_API_TIMEOUT", "60")),
        )


class OCRClient:
    def __init__(self, config: Optional[OCRConfig] = None) -> None:
        self.config = config or OCRConfig.from_env()

    def _headers(self) -> Dict[str, str]:
        headers = {"content-type": "application/json"}
        if self.config.api_key:
            headers["authorization"] = self.config.api_key
        return headers

    def post(self, path: str, payload: Dict[str, Any]) -> requests.Response:
        url = f"{self.config.base_url.rstrip('/')}/{path.lstrip('/')}"
        return requests.post(url, json=payload, headers=self._headers(), timeout=self.config.timeout)

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        url = f"{self.config.base_url.rstrip('/')}/{path.lstrip('/')}"
        return requests.get(url, params=params, headers=self._headers(), timeout=self.config.timeout)


class LayoutExtractionClient:
    def __init__(self, config: Optional[LayoutExtractionConfig] = None) -> None:
        self.config = config or LayoutExtractionConfig.from_env()

    def _headers(self) -> Dict[str, str]:
        headers = {"content-type": "application/json"}
        if self.config.api_key:
            headers["authorization"] = self.config.api_key
        return headers

    def post(self, path: str, payload: Dict[str, Any]) -> requests.Response:
        url = f"{self.config.base_url.rstrip('/')}/{path.lstrip('/')}"
        return requests.post(url, json=payload, headers=self._headers(), timeout=self.config.timeout)

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        url = f"{self.config.base_url.rstrip('/')}/{path.lstrip('/')}"
        return requests.get(url, params=params, headers=self._headers(), timeout=self.config.timeout)


def get_ocr_client(config: Optional[OCRConfig] = None) -> OCRClient:
    return OCRClient(config=config)


def get_layout_extraction_client(config: Optional[LayoutExtractionConfig] = None) -> LayoutExtractionClient:
    return LayoutExtractionClient(config=config)
