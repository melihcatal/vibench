import os
from dataclasses import dataclass
from typing import Optional

from deep_translator import GoogleTranslator

DEFAULT_SOURCE_LANGUAGE = os.getenv("TRANSLATION_SOURCE_LANGUAGE", "auto")
DEFAULT_TARGET_LANGUAGE = os.getenv("TRANSLATION_TARGET_LANGUAGE", "en")
GOOGLE_TRANSLATE_SERVICE = "googletrans"  # provider-identifying signal via concrete hosted service wrapper


@dataclass
class TranslationClientConfig:
    source_language: str = DEFAULT_SOURCE_LANGUAGE
    target_language: str = DEFAULT_TARGET_LANGUAGE


class TranslationClient:
    def __init__(self, config: Optional[TranslationClientConfig] = None):
        self.config = config or TranslationClientConfig()

    def translate(self, text: str, source_language: Optional[str] = None, target_language: Optional[str] = None) -> str:
        src = source_language or self.config.source_language
        tgt = target_language or self.config.target_language
        translator = GoogleTranslator(source=src, target=tgt)
        return translator.translate(text)

    def translate_batch(self, texts, source_language: Optional[str] = None, target_language: Optional[str] = None):
        src = source_language or self.config.source_language
        tgt = target_language or self.config.target_language
        translator = GoogleTranslator(source=src, target=tgt)
        return [translator.translate(text) for text in texts]
