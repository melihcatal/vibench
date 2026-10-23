from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

import requests

from document_models import OCRResponse, normalize_ocr_response, normalize_ocr_text


@dataclass(frozen=True)
class OCRTranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass(frozen=True)
class OCRTranslationResponse:
    text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    raw: Any = None


@dataclass(frozen=True)
class AzureTranslatorConfig:
    endpoint: str
    key: Optional[str]
    region: Optional[str]
    api_version: str
    timeout: float


def _env(name: str, default: str = "") -> str:
    value = os.getenv(name)
    return value if value not in (None, "") else default


@lru_cache(maxsize=1)
def get_azure_translator_config() -> AzureTranslatorConfig:
    return AzureTranslatorConfig(
        endpoint=_env("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com").rstrip("/"),
        key=os.getenv("AZURE_TRANSLATOR_KEY"),
        region=os.getenv("AZURE_TRANSLATOR_REGION"),
        api_version=_env("AZURE_TRANSLATOR_API_VERSION", "3.0"),
        timeout=float(_env("AZURE_TRANSLATOR_TIMEOUT", "60")),
    )


class AzureOCRTranslator:
    def __init__(self, config: Optional[AzureTranslatorConfig] = None) -> None:
        self.config = config or get_azure_translator_config()
        self._session = requests.Session()

    def translate_text(self, request: OCRTranslationRequest) -> OCRTranslationResponse:
        if not request.text:
            return OCRTranslationResponse(text="", source_language=request.source_language, target_language=request.target_language, raw={"translations": []})
        if not self.config.key:
            raise ValueError("Missing Azure Translator key")
        headers = {
            "Ocp-Apim-Subscription-Key": self.config.key,
            "Content-Type": "application/json; charset=utf-8",
        }
        if self.config.region:
            headers["Ocp-Apim-Subscription-Region"] = self.config.region
        params: Dict[str, str] = {"api-version": self.config.api_version, "to": request.target_language}
        if request.source_language:
            params["from"] = request.source_language
        body = [{"text": request.text}]
        response = self._session.post(f"{self.config.endpoint}/translate", params=params, json=body, headers=headers, timeout=self.config.timeout)
        response.raise_for_status()
        data = response.json()
        translated = ""
        if isinstance(data, list) and data:
            translations = data[0].get("translations", []) if isinstance(data[0], dict) else []
            if translations:
                translated = normalize_ocr_text(translations[0].get("text"))
        return OCRTranslationResponse(text=translated, source_language=request.source_language, target_language=request.target_language, raw=data)

    def translate_ocr_response(self, response: OCRResponse, target_language: str, source_language: Optional[str] = None) -> OCRTranslationResponse:
        normalized = normalize_ocr_response(response)
        return self.translate_text(OCRTranslationRequest(text=normalized.text, target_language=target_language, source_language=source_language or normalized.language))


def translate_ocr_text(text: str, target_language: str, source_language: Optional[str] = None, config: Optional[AzureTranslatorConfig] = None) -> OCRTranslationResponse:
    return AzureOCRTranslator(config=config).translate_text(OCRTranslationRequest(text=normalize_ocr_text(text), target_language=target_language, source_language=source_language))


def translate_ocr_response(response: OCRResponse, target_language: str, source_language: Optional[str] = None, config: Optional[AzureTranslatorConfig] = None) -> OCRTranslationResponse:
    return AzureOCRTranslator(config=config).translate_ocr_response(response, target_language=target_language, source_language=source_language)
