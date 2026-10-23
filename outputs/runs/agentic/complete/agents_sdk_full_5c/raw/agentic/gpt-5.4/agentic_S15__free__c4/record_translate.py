from __future__ import annotations

from typing import Any, Dict, Iterable, List, Sequence

from deepl import DeepLClient

from database_models import TranslationResult


DEEPL_MODEL_TYPE = "quality_optimized"



def translate_record_fields(records: Iterable[Dict[str, Any]], target_language: str, fields: Sequence[str] = ("title", "content")) -> List[TranslationResult]:
    client = DeepLClient(auth_key=__import__("os").environ["DEEPL_AUTH_KEY"])
    translated_records: List[TranslationResult] = []
    for record in records:
        translated_fields: Dict[str, str] = {}
        for field in fields:
            value = record.get(field)
            if not value:
                continue
            result = client.translate_text(str(value), target_lang=target_language, model_type=DEEPL_MODEL_TYPE)
            translated_fields[field] = result.text
        translated_records.append(
            TranslationResult(
                document_id=str(record.get("id")),
                translated_fields=translated_fields,
                target_language=target_language,
            )
        )
    return translated_records
