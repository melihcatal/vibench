import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


@dataclass(frozen=True)
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: Optional[str] = None
    target_language: str = "en"
    provider: str = "openai"
    model: str = OPENAI_MODEL


def _normalize_note(note: Any) -> str:
    if note is None:
        return ""
    if isinstance(note, str):
        return note.strip()
    if isinstance(note, bytes):
        return note.decode("utf-8", errors="replace").strip()
    return str(note).strip()


def _build_messages(text: str, target_language: str, source_language: Optional[str]) -> List[Dict[str, str]]:
    instructions = [
        "Translate the following encryption or compliance note for reviewers.",
        f"Translate into {target_language}.",
        "Preserve technical meaning, key names, identifiers, and policy terminology.",
        "Return only the translated text.",
    ]
    if source_language:
        instructions.insert(1, f"The source language is {source_language}.")
    return [
        {"role": "system", "content": "You are a precise compliance translation assistant."},
        {"role": "user", "content": "\n".join(instructions + ["", text])},
    ]


def _openai_translate(text: str, api_key: str, target_language: str, source_language: Optional[str], timeout: int) -> str:
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": OPENAI_MODEL, "messages": _build_messages(text, target_language, source_language), "temperature": 0},
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()
    choices = payload.get("choices", [])
    if not choices:
        raise ValueError("OpenAI translation response contained no choices")
    message = choices[0].get("message", {})
    content = message.get("content", "")
    if not content:
        raise ValueError("OpenAI translation response contained no content")
    return content.strip()


def translate_compliance_note(note: Any, target_language: str = "en", source_language: Optional[str] = None, api_key: Optional[str] = None, timeout: int = 30) -> TranslationResult:
    text = _normalize_note(note)
    if not text:
        raise ValueError("note must not be empty")
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    translated = _openai_translate(text, key, target_language, source_language, timeout)
    return TranslationResult(source_text=text, translated_text=translated, source_language=source_language, target_language=target_language)


def translate_compliance_notes(notes: Iterable[Any], target_language: str = "en", source_language: Optional[str] = None, api_key: Optional[str] = None, timeout: int = 30) -> List[TranslationResult]:
    return [translate_compliance_note(note, target_language=target_language, source_language=source_language, api_key=api_key, timeout=timeout) for note in notes]
