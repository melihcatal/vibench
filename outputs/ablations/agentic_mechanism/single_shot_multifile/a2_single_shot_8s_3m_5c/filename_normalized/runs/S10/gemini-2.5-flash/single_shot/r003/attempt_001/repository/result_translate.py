from model_client import LLMClientFactory
from model_models import TranslationRequest, TranslatedTextResponse
import os

GOOGLE_CLOUD_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")

def translate_model_output(request: TranslationRequest) -> TranslatedTextResponse:
    client = LLMClientFactory.get_google_translate_client()

    parent = f"projects/{GOOGLE_CLOUD_PROJECT_ID}" if GOOGLE_CLOUD_PROJECT_ID else ""

    response = client.translate_text(
        parent=parent,
        contents=[request.text],
        target_language_code=request.target_language,
        source_language_code=request.source_language,
        mime_type="text/plain"
    )

    translated_text = ""
    detected_source_language = None

    if response.translations:
        translated_text = response.translations[0].translated_text
        detected_source_language = response.translations[0].detected_language_code

    return TranslatedTextResponse(
        translated_text=translated_text,
        detected_source_language=detected_source_language
    )