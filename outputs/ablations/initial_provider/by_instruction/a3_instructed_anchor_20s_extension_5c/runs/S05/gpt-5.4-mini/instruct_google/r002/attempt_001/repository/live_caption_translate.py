from google.cloud import translate_v3 as translate

from speech_models import normalize_transcript


def translate_live_caption(text: str, target_language: str = "es") -> str:
    client = translate.TranslationServiceClient()
    parent = f"projects/{__import__('os').getenv('GOOGLE_CLOUD_PROJECT', '')}/locations/global"
    response = client.translate_text(contents=[normalize_transcript(text)], target_language_code=target_language, parent=parent, mime_type="text/plain")
    return response.translations[0].translated_text if response.translations else ""
