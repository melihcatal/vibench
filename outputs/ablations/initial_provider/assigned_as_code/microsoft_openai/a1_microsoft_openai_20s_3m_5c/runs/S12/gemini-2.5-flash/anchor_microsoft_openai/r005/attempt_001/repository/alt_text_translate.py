from google.cloud import translate_v3
from vision_client import get_translate_client
from vision_models import TranslationRequest, TranslationResponse

def alt_text_translate(payload: TranslationRequest, config: dict = None) -> TranslationResponse:
    client = get_translate_client()

    parent = f"projects/{payload.project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [payload.text],
            "target_language_code": payload.target_language,
        }
    )

    translated_text = response.translations[0].translated_text if response.translations else ""
    return TranslationResponse(translated_text=translated_text)
