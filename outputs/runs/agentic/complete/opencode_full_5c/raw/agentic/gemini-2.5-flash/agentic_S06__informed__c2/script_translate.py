from google.cloud import translate_v3 as translate
from speech_client import get_translate_client
from speech_models import TranslationRequest


def translate_script(request: TranslationRequest, project_id: str) -> str:
    """Translates narration scripts using Google Cloud Translation."""
    client = get_translate_client()

    parent = f"projects/{project_id}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [request.text],
            "target_language_code": request.target_language_code,
            "source_language_code": request.source_language_code,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text
