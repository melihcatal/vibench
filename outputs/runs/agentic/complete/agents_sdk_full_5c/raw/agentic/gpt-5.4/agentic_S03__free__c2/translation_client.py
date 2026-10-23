from __future__ import annotations

import os
from typing import Sequence

from google.cloud import translate_v2 as translate
from openai import OpenAI


GOOGLE_TRANSLATE_PROVIDER = "google_translate"
OPENAI_PROVIDER = "openai"
OPENAI_QUALITY_MODEL = os.getenv("OPENAI_QUALITY_MODEL", "gpt-4o-mini")
OPENAI_SAFETY_MODEL = os.getenv("OPENAI_SAFETY_MODEL", "gpt-4o-mini")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
GOOGLE_TTS_VOICE = os.getenv("GOOGLE_TTS_VOICE", "en-US-Standard-C")


def get_google_translate_client() -> translate.Client:
    return translate.Client()


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def detect_mime_type(text: str) -> str:
    lowered = text.lower()
    if "<html" in lowered or "<div" in lowered or "<span" in lowered or "<p" in lowered:
        return "text/html"
    return "text/plain"


def split_languages(voice_name: str) -> tuple[str, str]:
    parts = voice_name.split("-")
    if len(parts) >= 2:
        return parts[0], parts[1]
    return "en", "US"


def build_quality_prompt(source_text: str, translated_text: str, source_language: str, target_language: str) -> str:
    return (
        "Review the translation for accuracy, fluency, terminology, omissions, and formatting. "
        "Return a concise summary followed by a short bullet list of issues.\n"
        f"Source language: {source_language}\n"
        f"Target language: {target_language}\n"
        f"Source text: {source_text}\n"
        f"Translated text: {translated_text}"
    )


def build_safety_prompt(texts: Sequence[str], language: str) -> str:
    joined = "\n".join(f"- {text}" for text in texts)
    return (
        "Assess whether the following localized copy contains unsafe content such as self-harm, sexual content involving minors, explicit violence, hateful harassment, or instructions facilitating wrongdoing. "
        "Respond with SAFE or UNSAFE on the first line, then list category labels separated by commas on the second line.\n"
        f"Language: {language}\n"
        f"Copy items:\n{joined}"
    )
