import os

from google.cloud import translate_v3 as translate

from identity_models import normalize_locale


def welcome_translate(text: str, locale: str | None = None):
    client = translate.TranslationServiceClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    parent = f"projects/{project_id}/locations/global"
    response = client.translate_text(
        contents=[text],
        target_language_code=normalize_locale(locale),
        parent=parent,
        mime_type="text/plain",
    )
    return response.translations[0].translated_text
