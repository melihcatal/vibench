import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI


DEFAULT_MODEL = os.getenv("TRANSLATION_MODEL", "gpt-4o-mini")
DEFAULT_SOURCE_LANG = os.getenv("TRANSLATION_SOURCE_LANGUAGE", "auto")
DEFAULT_TARGET_LANG = os.getenv("TRANSLATION_TARGET_LANGUAGE", "en")


@dataclass(frozen=True)
class TranslationConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: str = DEFAULT_MODEL
    source_language: str = DEFAULT_SOURCE_LANG
    target_language: str = DEFAULT_TARGET_LANG
    temperature: float = 0.0

    @classmethod
    def from_env(cls) -> "TranslationConfig":
        return cls(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
            model=os.getenv("TRANSLATION_MODEL", DEFAULT_MODEL),
            source_language=os.getenv("TRANSLATION_SOURCE_LANGUAGE", DEFAULT_SOURCE_LANG),
            target_language=os.getenv("TRANSLATION_TARGET_LANGUAGE", DEFAULT_TARGET_LANG),
            temperature=float(os.getenv("TRANSLATION_TEMPERATURE", "0")),
        )


class TranslationClient:
    def __init__(self, config: Optional[TranslationConfig] = None) -> None:
        self.config = config or TranslationConfig.from_env()
        self.client = OpenAI(api_key=self.config.api_key, base_url=self.config.base_url)

    def translate_text(
        self,
        text: str,
        source_language: Optional[str] = None,
        target_language: Optional[str] = None,
        model: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> str:
        if not text:
            return ""

        response = self.client.responses.create(
            model=model or self.config.model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are a precise translation engine. "
                        "Translate the user's text faithfully without adding explanations."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Source language: {source_language or self.config.source_language}\n"
                        f"Target language: {target_language or self.config.target_language}\n"
                        f"Text:\n{text}"
                    ),
                },
            ],
            temperature=self.config.temperature,
            **(extra or {}),
        )
        return getattr(response, "output_text", "").strip()


def get_translation_config() -> TranslationConfig:
    return TranslationConfig.from_env()


def get_translation_client() -> TranslationClient:
    return TranslationClient()


def translate_text(
    text: str,
    source_language: Optional[str] = None,
    target_language: Optional[str] = None,
    model: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> str:
    return get_translation_client().translate_text(
        text=text,
        source_language=source_language,
        target_language=target_language,
        model=model,
        extra=extra,
    )
