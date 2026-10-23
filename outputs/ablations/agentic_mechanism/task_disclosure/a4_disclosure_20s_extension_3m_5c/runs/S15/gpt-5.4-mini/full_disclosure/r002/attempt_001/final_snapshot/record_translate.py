from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
DEFAULT_OPENAI_MODEL = "gpt-5.4-mini"


@dataclass
class TranslationResult:
    translated_fields: Dict[str, Any]
    source_language: Optional[str] = None
    target_language: Optional[str] = None


def _deep_copy(value: Any) -> Any:
    return json.loads(json.dumps(value))


def _iter_text_fields(document: Mapping[str, Any], field_paths: Optional[Sequence[str]]) -> Iterable[str]:
    if field_paths:
        for path in field_paths:
            yield path
        return
    for key, value in document.items():
        if isinstance(value, str) and value.strip():
            yield key


def _get_path(document: Mapping[str, Any], path: str) -> Any:
    current: Any = document
    for part in path.split("."):
        if not isinstance(current, Mapping) or part not in current:
            return None
        current = current[part]
    return current


def _set_path(document: MutableMapping[str, Any], path: str, value: Any) -> None:
    parts = path.split(".")
    current: MutableMapping[str, Any] = document
    for part in parts[:-1]:
        nxt = current.get(part)
        if not isinstance(nxt, MutableMapping):
            nxt = {}
            current[part] = nxt
        current = nxt
    current[parts[-1]] = value


def _translate_text_openai(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    model = os.getenv("OPENAI_MODEL", DEFAULT_OPENAI_MODEL)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    instruction = f"Translate the given text into {target_language}. Return only the translated text."
    if source_language:
        instruction = f"Translate the given text from {source_language} into {target_language}. Return only the translated text."
    payload = {
        "model": model,
        "input": [
            {
                "role": "system",
                "content": [{"type": "text", "text": instruction}],
            },
            {
                "role": "user",
                "content": [{"type": "text", "text": text}],
            },
        ],
    }
    response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    texts: List[str] = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"} and content.get("text"):
                texts.append(content["text"])
    translated = "".join(texts).strip()
    if not translated:
        raise RuntimeError("OpenAI translation response was empty")
    return translated


def translate_record(document: Mapping[str, Any], target_language: str, field_paths: Optional[Sequence[str]] = None, source_language: Optional[str] = None) -> TranslationResult:
    translated = _deep_copy(document)
    for path in _iter_text_fields(document, field_paths):
        value = _get_path(document, path)
        if isinstance(value, str) and value.strip():
            _set_path(translated, path, _translate_text_openai(value, target_language, source_language))
    return TranslationResult(translated_fields=translated, source_language=source_language, target_language=target_language)


def handler(event: Mapping[str, Any], context: Any = None) -> Dict[str, Any]:
    document = event.get("document")
    if not isinstance(document, Mapping):
        raise ValueError("event.document must be an object")
    target_language = event.get("target_language")
    if not isinstance(target_language, str) or not target_language.strip():
        raise ValueError("event.target_language must be a non-empty string")
    field_paths = event.get("field_paths")
    if field_paths is not None and not isinstance(field_paths, Sequence):
        raise ValueError("event.field_paths must be a sequence if provided")
    source_language = event.get("source_language")
    result = translate_record(document, target_language.strip(), field_paths=field_paths, source_language=source_language if isinstance(source_language, str) else None)
    return {
        "translated_document": result.translated_fields,
        "source_language": result.source_language,
        "target_language": result.target_language,
        "provider": "openai",
        "model": os.getenv("OPENAI_MODEL", DEFAULT_OPENAI_MODEL),
    }
