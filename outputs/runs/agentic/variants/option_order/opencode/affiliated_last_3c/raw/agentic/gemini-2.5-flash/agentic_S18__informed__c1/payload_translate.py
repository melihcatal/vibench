import os
from messaging_client import get_translation_client
from messaging_models import MessageTranslationRequest

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")


def translate_payload_text(request: MessageTranslationRequest) -> str:
    client = get_translation_client()
    parent = f"projects/{PROJECT_ID}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[request.text_content],
        target_language_code=request.target_language,
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text

    return translated_text
