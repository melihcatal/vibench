from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from deepL import Translator as _DeepLTranslator

from translation_models import normalize_text, normalize_text_list

PROVIDER_NAME = 'DeepL'
DEFAULT_MODEL = 'deepl-api'


@lru_cache(maxsize=1)
def get_client() -> _DeepLTranslator:
    auth_key = os.environ['DEEPL_AUTH_KEY']
    return _DeepLTranslator(auth_key)


def get_default_source_language() -> str:
    return os.getenv('TRANSLATION_SOURCE_LANGUAGE', 'en')


def get_default_target_language() -> str:
    return os.getenv('TRANSLATION_TARGET_LANGUAGE', 'es')


def prepare_text(value: str) -> str:
    return normalize_text(value)


def prepare_texts(values):
    return normalize_text_list(values)
