import os

from google.cloud import translate_v3

from identity_models import normalize_locale


def welcome_translate(text: str, locale: str) -> str:
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{os.environ['GOOGLE_CLOUD_PROJECT']}/locations/global"
    response = client.translate_text(
        contents=[text],
        target_language_code=normalize_locale(locale),
        parent=parent,
        mime_type="text/plain",
    )
    return response.translations[0].translated_text if response.translations else text
