import os
from dataclasses import dataclass
from typing import Optional

from deepl import Translator

from translation_models import normalize_language_code


@dataclass
class TranslationClientConfig:
    auth_key: str
    api_url: str | None = None


def load_translation_config() -> TranslationClientConfig:
    auth_key = os.environ['DEEPL_AUTH_KEY']
    api_url = os.getenv('DEEPL_API_URL')
    return TranslationClientConfig(auth_key=auth_key, api_url=api_url)


def create_translation_client(config: Optional[TranslationClientConfig] = None) -> Translator:
    config = config or load_translation_config()
    if config.api_url:
        return Translator(config.auth_key, server_url=config.api_url)
    return Translator(config.auth_key)


def target_language_code(language: str) -> str:
    return normalize_language_code(language).replace('-', '_').upper()
