import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TranslationConfig:
    deepl_auth_key: str = field(
        default_factory=lambda: os.environ.get("DEEPL_AUTH_KEY", "")
    )
    deepl_api_url: str = "https://api-free.deepl.com/v2"
    default_source_lang: str = ""
    default_target_lang: str = "en"
    preserve_formatting: bool = True
    tag_handling: str = "html"
    split_sentences: str = "1"

    def __post_init__(self):
        if not self.deepl_auth_key:
            raise ValueError("DEEPL_AUTH_KEY environment variable must be set")


def get_config() -> TranslationConfig:
    return TranslationConfig()


def get_deepl_client():
    import deepl

    config = get_config()
    return deepl.Translator(config.deepl_auth_key, server_url=config.deepl_api_url)
