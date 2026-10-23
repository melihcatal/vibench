import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class TranslationConfig:
    auth_key: str
    api_hostname: str = "api-free.deepl.com"


@lru_cache(maxsize=1)
def get_config() -> TranslationConfig:
    return TranslationConfig(auth_key=os.environ["DEEPL_AUTH_KEY"])


def normalize_language_code(language: str) -> str:
    return language.replace("_", "-").strip()
