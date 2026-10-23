from __future__ import annotations

from messaging_client import translate_client
from messaging_models import normalize_text_payload


def translate_payload_text(message: dict, target_language_code: str) -> dict[str, str]:
    source_text = normalize_text_payload(message)
    response = translate_client().translate_text(
        Text=source_text,
        SourceLanguageCode="auto",
        TargetLanguageCode=target_language_code,
    )
    return {
        "provider": "aws_translate",
        "source_text": source_text,
        "translated_text": response["TranslatedText"],
        "target_language_code": target_language_code,
    }
