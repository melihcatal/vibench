import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI


@dataclass(frozen=True)
class TranslationConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: str = "gpt-5.4-mini"
    source_language: Optional[str] = None
    target_language: str = "en"

    @classmethod
    def from_env(cls) -> "TranslationConfig":
        return cls(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
            model=os.getenv("TRANSLATION_MODEL", "gpt-5.4-mini"),
            source_language=os.getenv("TRANSLATION_SOURCE_LANGUAGE"),
            target_language=os.getenv("TRANSLATION_TARGET_LANGUAGE", "en"),
        )


class TranslationClient:
    def __init__(self, config: Optional[TranslationConfig] = None) -> None:
        self.config = config or TranslationConfig.from_env()
        self._client = OpenAI(api_key=self.config.api_key, base_url=self.config.base_url)

    def translate(self, text: str, source_language: Optional[str] = None, target_language: Optional[str] = None) -> str:
        source = source_language or self.config.source_language
        target = target_language or self.config.target_language
        prompt = self._build_prompt(text, source, target)
        response = self._client.responses.create(
            model=self.config.model,
            input=prompt,
        )
        return self._extract_text(response)

    def _build_prompt(self, text: str, source_language: Optional[str], target_language: str) -> str:
        if source_language:
            return f"Translate the following text from {source_language} to {target_language}. Return only the translated text.\n\n{text}"
        return f"Translate the following text to {target_language}. Return only the translated text.\n\n{text}"

    def _extract_text(self, response: Any) -> str:
        if hasattr(response, "output_text") and response.output_text:
            return response.output_text
        if hasattr(response, "output"):
            parts = []
            for item in response.output:
                content = getattr(item, "content", None)
                if content:
                    for part in content:
                        text = getattr(part, "text", None)
                        if text:
                            parts.append(text)
            if parts:
                return "".join(parts)
        raise RuntimeError("Translation response did not contain text")


def get_translation_client(config_overrides: Optional[Dict[str, Any]] = None) -> TranslationClient:
    config = TranslationConfig.from_env()
    if config_overrides:
        config = TranslationConfig(
            api_key=config_overrides.get("api_key", config.api_key),
            base_url=config_overrides.get("base_url", config.base_url),
            model=config_overrides.get("model", config.model),
            source_language=config_overrides.get("source_language", config.source_language),
            target_language=config_overrides.get("target_language", config.target_language),
        )
    return TranslationClient(config)
