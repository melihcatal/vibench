"""Translation client helper utilities for General Text Translation.

Provides configuration loading, client initialization, and retry logic
for the DeepL translation API.
"""

import os
import time
from dataclasses import dataclass, field
from typing import Any

import deepl
from deepl import Translator, DeepLException


@dataclass
class TranslationConfig:
    """Configuration for DeepL translation client."""

    auth_key: str = field(default_factory=lambda: os.environ.get("DEEPL_AUTH_KEY", ""))
    server_url: str = "https://api.deepl.com"
    max_retries: int = 3
    retry_delay: float = 1.0
    proxy_url: str | None = None

    @classmethod
    def from_env(cls) -> "TranslationConfig":
        """Load configuration from environment variables."""
        return cls(
            auth_key=os.environ.get("DEEPL_AUTH_KEY", ""),
            server_url=os.environ.get("DEEPL_SERVER_URL", "https://api.deepl.com"),
            max_retries=int(os.environ.get("DEEPL_MAX_RETRIES", "3")),
            retry_delay=float(os.environ.get("DEEPL_RETRY_DELAY", "1.0")),
            proxy_url=os.environ.get("DEEPL_PROXY_URL") or None,
        )

    def is_valid(self) -> bool:
        """Check if required configuration is present."""
        return bool(self.auth_key)


class TranslationClient:
    """Wrapper around the DeepL Translator with retry and error handling."""

    def __init__(self, config: TranslationConfig | None = None):
        self.config = config or TranslationConfig.from_env()
        if not self.config.is_valid():
            raise ValueError(
                "DeepL auth key is required. Set DEEPL_AUTH_KEY environment variable."
            )
        self._translator = Translator(
            auth_key=self.config.auth_key,
            server_url=self.config.server_url,
            proxy=self.config.proxy_url,
        )

    @property
    def translator(self) -> Translator:
        """Return the underlying DeepL Translator instance."""
        return self._translator

    def translate_with_retry(
        self,
        text: str | list[str],
        target_lang: str,
        source_lang: str | None = None,
        **kwargs: Any,
    ) -> list[deepl.TextResult]:
        """Execute translation with automatic retry on transient errors.

        Args:
            text: Single string or list of strings to translate.
            target_lang: Target language code.
            source_lang: Source language code (auto-detect if None).
            **kwargs: Additional kwargs passed to DeepL translator.

        Returns:
            List of TextResult objects from DeepL.
        """
        last_exception: Exception | None = None
        for attempt in range(self.config.max_retries):
            try:
                call_kwargs: dict[str, Any] = {"target_lang": target_lang}
                if source_lang:
                    call_kwargs["source_lang"] = source_lang
                call_kwargs.update(kwargs)

                result = self._translator.translate_text(text, **call_kwargs)
                if isinstance(result, deepl.TextResult):
                    return [result]
                return result
            except DeepLException as exc:
                last_exception = exc
                if attempt < self.config.max_retries - 1:
                    time.sleep(self.config.retry_delay * (attempt + 1))
        raise last_exception  # type: ignore[misc]

    def get_usage(self) -> dict[str, Any]:
        """Get current DeepL API usage statistics."""
        try:
            usage = self._translator.get_usage()
            return {
                "character_count": usage.character.count if hasattr(usage, "character") else None,
                "character_limit": usage.character.limit if hasattr(usage, "character") else None,
                "document_count": usage.document.count if hasattr(usage, "document") else None,
                "document_limit": usage.document.limit if hasattr(usage, "document") else None,
                "team_document_count": usage.team_document.count if hasattr(usage, "team_document") else None,
            }
        except DeepLException:
            return {}

    def get_source_languages(self) -> list[dict[str, str]]:
        """Get list of supported source languages."""
        langs = self._translator.get_source_languages()
        return [{"code": lang.code, "name": lang.name} for lang in langs]

    def get_target_languages(self) -> list[dict[str, str]]:
        """Get list of supported target languages."""
        langs = self._translator.get_target_languages()
        return [{"code": lang.code, "name": lang.name, "formality": getattr(lang, "supports_formality", None)} for lang in langs]
