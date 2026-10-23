import os
from typing import Dict, Iterable, Optional

from openai import OpenAI


def load_tts_config() -> Dict[str, str]:
    return {
        "provider": os.getenv("TTS_PROVIDER", "openai"),
        "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
        "openai_tts_model": os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts"),
        "openai_transcribe_model": os.getenv("OPENAI_TRANSCRIBE_MODEL", "gpt-4o-mini-transcribe"),
        "openai_translate_model": os.getenv("OPENAI_TRANSLATE_MODEL", "gpt-4o-mini-transcribe"),
        "openai_embed_model": os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small"),
        "azure_speech_key": os.getenv("AZURE_SPEECH_KEY", ""),
        "azure_speech_region": os.getenv("AZURE_SPEECH_REGION", ""),
    }


def openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def preferred_voice(locale: str) -> str:
    locale = (locale or "").lower()
    mapping = {
        "en-us": "alloy",
        "en-gb": "verse",
        "es-es": "nova",
        "fr-fr": "shimmer",
        "de-de": "echo",
    }
    return mapping.get(locale, "alloy")


def chunk_text(text: str, max_chars: int = 4000) -> Iterable[str]:
    text = text or ""
    for start in range(0, len(text), max_chars):
        yield text[start : start + max_chars]
