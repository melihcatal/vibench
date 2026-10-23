from google.cloud import translate_v2 as translate
from observability_models import TranslationRequest
from observability_client import get_project_id


def translate_note(request: TranslationRequest) -> dict:
    """
    Translates metric or dashboard notes for another locale using Google Cloud Translate.
    """
    client = translate.Client()
    project_id = get_project_id()

    result = client.translate(request.text, target_language=request.target_locale)

    return {
        "original_text": request.text,
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
        "target_locale": request.target_locale,
    }
