import os
from dataclasses import dataclass

from deepl import Translator


@dataclass(frozen=True)
class TranslationConfig:
    auth_key: str
    source_lang: str | None = None
    target_lang: str = "EN-US"


def load_translation_config(
    source_lang: str | None = None, target_lang: str = "EN-US"
) -> TranslationConfig:
    auth_key = os.environ["DEEPL_AUTH_KEY"]
    return TranslationConfig(
        auth_key=auth_key, source_lang=source_lang, target_lang=target_lang
    )


def create_translation_client(config: TranslationConfig) -> Translator:
    return Translator(config.auth_key)


def normalize_language_code(language: str | None) -> str | None:
    if language is None:
        return None
    return language.replace("_", "-").upper()
