import os
from typing import Optional

from speech_models import SpeechConfig


def load_speech_config(provider: str, language: str = "en-US", punctuation: bool = True, model: Optional[str] = None) -> SpeechConfig:
    provider = provider.lower()
    if provider == "azure":
        return SpeechConfig(
            provider="azure",
            language=language,
            punctuation=punctuation,
            api_key=os.getenv("AZURE_SPEECH_KEY"),
            region=os.getenv("AZURE_SPEECH_REGION"),
            model=model,
        )
    return SpeechConfig(
        provider="openai",
        language=language,
        punctuation=punctuation,
        api_key=os.getenv("OPENAI_API_KEY"),
        model=model or os.getenv("OPENAI_TRANSCRIBE_MODEL", "gpt-4o-mini-transcribe"),
    )


def provider_name(config: SpeechConfig) -> str:
    return config.provider
