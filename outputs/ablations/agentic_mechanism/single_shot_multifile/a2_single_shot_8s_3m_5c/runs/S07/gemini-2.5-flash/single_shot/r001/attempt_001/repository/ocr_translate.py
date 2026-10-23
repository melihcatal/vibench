from google.cloud import translate_v3
from document_client import get_translation_client, get_project_id
from document_models import TranslatedTextResult

def translate_ocr_text(text: str, target_language_code: str, source_language_code: str = "auto") -> TranslatedTextResult:
    client = get_translation_client()
    project_id = get_project_id()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"
    if source_language_code == "auto":
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language_code,
            }
        )
    else:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "source_language_code": source_language_code,
                "target_language_code": target_language_code,
            }
        )
    translated_text = response.translations[0].translated_text
    detected_source_language = response.translations[0].detected_language_code
    return TranslatedTextResult(
        translated_text=translated_text,
        source_language_code=detected_source_language,
        target_language_code=target_language_code
    )