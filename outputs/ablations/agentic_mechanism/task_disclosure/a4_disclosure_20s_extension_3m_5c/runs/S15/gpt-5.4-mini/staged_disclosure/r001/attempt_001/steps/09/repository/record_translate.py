import os
from typing import Any, Dict, Iterable, List, Optional

from openai import OpenAI


MODEL_ID = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


class RecordTranslator:
    def __init__(self, client: Optional[OpenAI] = None) -> None:
        self.client = client or OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def translate_field(self, text: str, target_language: str) -> str:
        if not text:
            return text
        response = self.client.responses.create(
            model=MODEL_ID,
            input=[
                {
                    "role": "system",
                    "content": f"Translate user-facing document text into {target_language}. Preserve meaning, formatting, identifiers, and numbers. Return only the translated text.",
                },
                {"role": "user", "content": text},
            ],
        )
        return response.output_text.strip()

    def translate_record(
        self,
        record: Dict[str, Any],
        fields: Iterable[str],
        target_language: str,
    ) -> Dict[str, Any]:
        translated = dict(record)
        for field in fields:
            value = translated.get(field)
            if isinstance(value, str):
                translated[field] = self.translate_field(value, target_language)
            elif isinstance(value, list):
                translated[field] = [
                    self.translate_field(item, target_language) if isinstance(item, str) else item
                    for item in value
                ]
        return translated


def translate_user_facing_document_fields(
    record: Dict[str, Any],
    fields: Iterable[str],
    target_language: str,
    client: Optional[OpenAI] = None,
) -> Dict[str, Any]:
    return RecordTranslator(client=client).translate_record(record, fields, target_language)
