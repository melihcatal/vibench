import os
from google.cloud import translate_v2 as translate
from database_models import DocumentResponse, TranslationRecord

GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
GOOGLE_TRANSLATE_PROJECT_ID = os.environ.get("GOOGLE_TRANSLATE_PROJECT_ID", "")


def translate_records(
    documents: list[DocumentResponse],
    target_language: str,
    fields: list[str] = None,
) -> list[TranslationRecord]:
    client = translate.Client()
    translations = []

    for doc in documents:
        fields_to_translate = fields or list(doc.data.keys())
        for field_name in fields_to_translate:
            field_value = doc.data.get(field_name, "")
            if not isinstance(field_value, str) or not field_value.strip():
                continue

            result = client.translate(
                field_value,
                target_language=target_language,
                format_="text",
            )

            translations.append(
                TranslationRecord(
                    document_id=doc.document_id,
                    field_name=field_name,
                    original_text=field_value,
                    translated_text=result["translatedText"],
                    source_language=result.get("detectedSourceLanguage", "unknown"),
                    target_language=target_language,
                )
            )

    return translations
