import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import deepl


@dataclass
class TranslationConfig:
    auth_key: str
    formality: Optional[str] = None
    preserve_formatting: bool = True


@lru_cache(maxsize=1)
def get_config() -> TranslationConfig:
    return TranslationConfig(
        auth_key=os.environ.get('DEEPL_AUTH_KEY', ''),
        formality=os.environ.get('DEEPL_FORMALITY') or None,
        preserve_formatting=os.environ.get('DEEPL_PRESERVE_FORMATTING', 'true').lower() == 'true',
    )


@lru_cache(maxsize=1)
def get_client() -> deepl.Translator:
    config = get_config()
    return deepl.Translator(config.auth_key)
