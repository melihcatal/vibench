"""Local configuration and client helper utilities for General Text Translation.

Provider: DeepL API (deepl SDK)
Auth: DEEPL_AUTH_KEY environment variable
"""

import os
from typing import Optional

import deepl


class TranslationClient:
    """Thin wrapper around the DeepL translation SDK with local config."""

    def __init__(
        self,
        auth_key: Optional[str] = None,
        server_url: Optional[str] = None,
    ) -> None:
        self.auth_key = auth_key or os.environ.get("DEEPL_AUTH_KEY", "")
        if not self.auth_key:
            raise ValueError("DEEPL_AUTH_KEY environment variable is required")
        self.client = deepl.Translator(self.auth_key)
        if server_url:
            self.client.server_url = server_url

    def get_usage(self) -> deepl.Usage:
        return self.client.get_usage()

    def translate(
        self,
        text: str,
        source_lang: str = "",
        target_lang: str = "EN",
        formality: str = "default",
        tag_handling: Optional[str] = None,
    ) -> deepl.TextResult:
        kwargs: dict = {
            "target_lang": target_lang.upper(),
        }
        if source_lang:
            kwargs["source_lang"] = source_lang.upper()
        if formality != "default":
            kwargs["formality"] = formality
        if tag_handling:
            kwargs["tag_handling"] = tag_handling
        return self.client.translate_text(text, **kwargs)

    def translate_list(
        self,
        texts: list[str],
        source_lang: str = "",
        target_lang: str = "EN",
        formality: str = "default",
        tag_handling: Optional[str] = None,
    ) -> list[deepl.TextResult]:
        kwargs: dict = {
            "target_lang": target_lang.upper(),
        }
        if source_lang:
            kwargs["source_lang"] = source_lang.upper()
        if formality != "default":
            kwargs["formality"] = formality
        if tag_handling:
            kwargs["tag_handling"] = tag_handling
        return self.client.translate_text(texts, **kwargs)


def get_client(auth_key: Optional[str] = None) -> TranslationClient:
    return TranslationClient(auth_key=auth_key)
