import os
from typing import Any, Dict, Optional

import requests

from translation_models import (
    BatchTranslationRequest,
    BatchTranslationResult,
    DictionaryTranslationRequest,
    DictionaryTranslationResult,
    MarkupTranslationRequest,
    MarkupTranslationResult,
    TranslationRequest,
    TranslationResult,
    normalize_translation_response,
)


DEEPL_API_HOST = os.getenv("DEEPL_API_HOST", "https://api-free.deepl.com")
DEEPL_AUTH_KEY_ENV = "DEEPL_AUTH_KEY"
DEEPL_MODEL_ID = "deepl-translation-api"


class TranslationServiceClient:
    def __init__(self, auth_key: Optional[str] = None, api_host: str = DEEPL_API_HOST, timeout: int = 30):
        self.auth_key = auth_key or os.getenv(DEEPL_AUTH_KEY_ENV, "")
        self.api_host = api_host.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def _request(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        headers = {"Authorization": f"DeepL-Auth-Key {self.auth_key}"}
        response = self.session.post(f"{self.api_host}{path}", data=payload, headers=headers, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def translate_text(self, request: TranslationRequest) -> TranslationResult:
        data = self._request("/v2/translate", {"text": request.text, "source_lang": request.source_language, "target_lang": request.target_language})
        return normalize_translation_response(data, TranslationResult)

    def batch_translate(self, request: BatchTranslationRequest) -> BatchTranslationResult:
        data = self._request("/v2/translate", {"text": request.texts, "source_lang": request.source_language, "target_lang": request.target_language})
        return normalize_translation_response(data, BatchTranslationResult)

    def translate_markup(self, request: MarkupTranslationRequest) -> MarkupTranslationResult:
        data = self._request("/v2/translate", {"text": request.markup, "source_lang": request.source_language, "target_lang": request.target_language, "tag_handling": "html"})
        return normalize_translation_response(data, MarkupTranslationResult)

    def translate_dictionary_values(self, request: DictionaryTranslationRequest) -> DictionaryTranslationResult:
        items = list(request.data.items())
        texts = [str(value) for _, value in items]
        data = self._request("/v2/translate", {"text": texts, "source_lang": request.source_language, "target_lang": request.target_language})
        translated = normalize_translation_response(data, BatchTranslationResult)
        return DictionaryTranslationResult(data={k: v for (k, _), v in zip(items, translated.translations)})


def get_translation_client() -> TranslationServiceClient:
    return TranslationServiceClient()
