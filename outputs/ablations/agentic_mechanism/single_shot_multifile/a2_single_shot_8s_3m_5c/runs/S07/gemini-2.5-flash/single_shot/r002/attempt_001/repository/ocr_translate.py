import os
import google.cloud.translate_v3 as translate

from document_client import get_google_translate_client
from document_models import TranslationResponse

def translate_ocr_text(text: str, target_language: str, source_language: Optional[str] = None) -> TranslationResponse:
    client = get_google_translate_client()
    project_id = os.environ.get("GOOGLE_TRANSLATE_PROJECT_ID")
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    request_params = {
        "parent": parent,
        "contents": [text],
        "target_language_code": target_language,
    }
    if source_language:
        request_params["source_language_code"] = source_language

    response = client.translate_text(request=request_params)

    translated_text = response.translations[0].translated_text if response.translations else ""
    detected_language = response.translations[0].detected_language_code if response.translations else None

    return TranslationResponse(translated_text=translated_text, detected_language_code=detected_language)
