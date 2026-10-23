import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name, default)
    return value if value else default


@dataclass
class TranslationConfig:
    source_language: str = 'auto'
    target_language: str = 'en'
    model: str = 'gpt-5.4-mini'
    api_key: Optional[str] = None

    @classmethod
    def from_env(cls) -> 'TranslationConfig':
        return cls(
            source_language=_env('TRANSLATION_SOURCE_LANGUAGE', 'auto'),
            target_language=_env('TRANSLATION_TARGET_LANGUAGE', 'en'),
            model=_env('OPENAI_TRANSLATION_MODEL', 'gpt-5.4-mini'),
            api_key=_env('OPENAI_API_KEY'),
        )


def get_client(api_key: Optional[str] = None) -> OpenAI:
    return OpenAI(api_key=api_key or _env('OPENAI_API_KEY'))


def build_instruction(source_language: str, target_language: str, preserve_markup: bool = False, preserve_keys: bool = False) -> str:
    parts = [f'Translate from {source_language} to {target_language}.']
    if preserve_markup:
        parts.append('Preserve all markup tags and attributes exactly.')
    if preserve_keys:
        parts.append('Preserve dictionary keys exactly and translate only values.')
    parts.append('Return only the translated result.')
    return ' '.join(parts)
