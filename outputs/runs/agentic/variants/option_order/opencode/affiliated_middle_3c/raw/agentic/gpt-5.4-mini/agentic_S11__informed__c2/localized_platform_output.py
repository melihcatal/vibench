import os
from google.cloud import translate_v3 as translate


def translate_platform_output(text: str, target_language: str) -> str:
    client = translate.TranslationServiceClient()
    parent = f"projects/{os.environ.get('GOOGLE_CLOUD_PROJECT', '')}/locations/global"
    response = client.translate_text(
        contents=[text],
        target_language_code=target_language,
        parent=parent,
        mime_type="text/plain",
    )
    return response.translations[0].translated_text
