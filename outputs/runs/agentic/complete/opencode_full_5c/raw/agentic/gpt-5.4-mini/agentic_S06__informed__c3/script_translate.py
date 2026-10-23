import os

from google.cloud import translate_v3


def translate_script(
    text: str, target_language: str, source_language: str = "en"
) -> str:
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{os.environ['GOOGLE_CLOUD_PROJECT']}/locations/global"
    response = client.translate_text(
        contents=[text],
        target_language_code=target_language,
        source_language_code=source_language,
        parent=parent,
    )
    return response.translations[0].translated_text
