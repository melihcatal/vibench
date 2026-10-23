from google.cloud import translate_v2 as translate
from document_client import get_google_translate_client
from document_models import TranslatedText


def translate_text(text: str, target_language: str) -> TranslatedText:
    translate_client = get_google_translate_client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return TranslatedText(
        translated_text=result["translatedText"],
        source_language=result["detectedSourceLanguage"],
    )
