from google.cloud import translate_v3 as translate
from document_client import get_translate_client
from document_models import DocumentConfig, TranslationResult


def ocr_translate(text: str, target_language: str, config: DocumentConfig) -> TranslationResult:
    client = get_translate_client()
    parent = f"projects/{config.project_id}/locations/{config.location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translations = response.translations
    if translations:
        first_translation = translations[0]
        return TranslationResult(
            translated_text=first_translation.translated_text,
            detected_language_code=first_translation.detected_language_code,
        )
    else:
        return TranslationResult(translated_text="")
