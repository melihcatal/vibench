from __future__ import annotations

from typing import Dict, Iterable, List, Optional
from deepl import DeepLClient
from database_models import DocumentRecord, TranslationResult, extract_text_fields


PROVIDER = "DeepL API"


def translate_record_fields(records: Iterable[DocumentRecord], target_language: str, field_names: Optional[List[str]] = None) -> List[TranslationResult]:
    client = DeepLClient(auth_key=__import__("os").getenv("DEEPL_AUTH_KEY"))
    results: List[TranslationResult] = []
    for record in records:
        text_fields = extract_text_fields(record.content, field_names=field_names)
        translated_fields: Dict[str, str] = {}
        for field_name, text in text_fields.items():
            translated = client.translate_text(text=text, target_lang=target_language)
            translated_fields[field_name] = translated.text
        results.append(
            TranslationResult(
                id=record.id,
                translated_fields=translated_fields,
                target_language=target_language,
                model="DeepL Translation API",
            )
        )
    return results
