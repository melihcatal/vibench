import os
from vision_client import get_translate_client
from vision_models import normalize_translation_response
from google.cloud.translate_v3 import TranslationServiceClient
from google.cloud.translate_v3.types import TranslateTextRequest

def alt_text_translate(text: str, target_language: str, project_id: str = None, config: dict = None) -> dict:
    client: TranslationServiceClient = get_translate_client()

    if not project_id:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT env var not set.")

    parent = f"projects/{project_id}/locations/global"

    request = TranslateTextRequest(
        parent=parent,
        contents=[text],
        target_language_code=target_language,
    )

    response = client.translate_text(request=request)
    translated_text = response.translations[0].translated_text

    return normalize_translation_response(translated_text)
