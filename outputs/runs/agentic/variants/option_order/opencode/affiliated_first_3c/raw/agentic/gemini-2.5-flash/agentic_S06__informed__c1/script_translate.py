from speech_client import TranslationClient
from speech_models import TranslateTextRequest, TranslateTextResponse
from google.cloud import translate_v3beta1 as translate
import os


def translate_script(text: str, target_language_code: str) -> TranslateTextResponse:
    """
    Translates narration scripts using Google Cloud Translation.
    """
    client_wrapper = TranslationClient()
    client = client_wrapper.client
    project_id = client_wrapper.project_id

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text

    return TranslateTextResponse(translated_text=translated_text)
