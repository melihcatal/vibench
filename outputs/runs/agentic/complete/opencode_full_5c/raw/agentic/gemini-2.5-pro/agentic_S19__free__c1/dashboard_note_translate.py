from google.cloud import translate_v2 as translate
from observability_models import TranslatedText


def translate_dashboard_note(text: str, target_language: str = "fr") -> TranslatedText:
    """
    Translates a dashboard note to another locale using Google Cloud Translate.
    """
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return TranslatedText(
        original_text=text,
        translated_text=result["translatedText"],
        target_language=target_language,
    )
