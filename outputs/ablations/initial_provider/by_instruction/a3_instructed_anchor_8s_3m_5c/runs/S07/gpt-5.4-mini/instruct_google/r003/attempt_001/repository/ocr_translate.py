import os

from google.cloud import translate_v3 as translate

from extract_text import extract_text


def ocr_translate(content: str, target_language: str, mime_type: str = "image/png") -> str:
    text = extract_text(content, mime_type=mime_type)
    client = translate.TranslationServiceClient()
    parent = f"projects/{os.environ['GOOGLE_CLOUD_PROJECT']}/locations/{os.environ.get('GOOGLE_CLOUD_LOCATION', 'global')}"
    response = client.translate_text(contents=[text], target_language_code=target_language, parent=parent)
    return response.translations[0].translated_text if response.translations else ""
