import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass(frozen=True)
class TranslationConfig:
    api_key: Optional[str] = None
    model: str = "gpt-4.1-mini"
    source_language: str = "auto"
    target_language: str = "en"


def load_translation_config() -> TranslationConfig:
    return TranslationConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini"),
        source_language=os.getenv("OPENAI_TRANSLATION_SOURCE_LANGUAGE", "auto"),
        target_language=os.getenv("OPENAI_TRANSLATION_TARGET_LANGUAGE", "en"),
    )


def create_translation_client(config: Optional[TranslationConfig] = None) -> OpenAI:
    cfg = config or load_translation_config()
    kwargs = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    return OpenAI(**kwargs)


def translate_script(text: str, config: Optional[TranslationConfig] = None) -> str:
    cfg = config or load_translation_config()
    client = create_translation_client(cfg)
    prompt = (
        f"Translate the following narration script from {cfg.source_language} to {cfg.target_language}. "
        "Preserve meaning, punctuation, line breaks, and narration style. Return only the translated script.\n\n"
        f"{text}"
    )
    response = client.responses.create(
        model=cfg.model,
        input=prompt,
    )
    return response.output_text.strip()
