from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from deepl import Translator

from translation_models import TranslationRequest, TranslationResult

PROVIDER_NAME = "DeepL"
DEFAULT_MODEL = "deepl-api"


@dataclass(frozen=True)
class TranslationClientConfig:
    auth_key: str


def load_config() -> TranslationClientConfig:
    auth_key = os.environ.get("DEEPL_AUTH_KEY", "")
    return TranslationClientConfig(auth_key=auth_key)


class TranslationClient:
    def __init__(self, config: Optional[TranslationClientConfig] = None) -> None:
        self.config = config or load_config()
        self._translator = Translator(self.config.auth_key) if self.config.auth_key else Translator("")

    def translate(self, request: TranslationRequest) -> TranslationResult:
        req = request.normalized()
        response = self._translator.translate_text(req.text, target_lang=req.target_language, source_lang=req.source_language or None)
        return TranslationResult(
            translated_text=str(response),
            source_language=req.source_language,
            target_language=req.target_language,
            provider=PROVIDER_NAME,
        )
