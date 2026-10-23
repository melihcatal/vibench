import os
from document_client import get_translation_client
from document_models import TranslationResponse

def translate_text(text: str, target_language: str, source_language: Optional[str] = None) -> TranslationResponse:
    client = get_translation_client()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION")

    if not all([project_id, location]):
        raise ValueError("Missing GOOGLE_CLOUD_PROJECT_ID or GOOGLE_CLOUD_LOCATION environment variables.")

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
            "source_language_code": source_language if source_language else None,
        }
    )

    translated_text = ""
    detected_language_code = None

    if response.translations:
        translated_text = response.translations[0].translated_text
        detected_language_code = response.translations[0].detected_language_code

    return TranslationResponse(translated_text=translated_text, detected_language_code=detected_language_code)
