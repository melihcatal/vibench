from google.cloud import translate_v2 as translate
from identity_models import WelcomeTranslatePayload
from typing import Dict, Any


def welcome_translate(payload: WelcomeTranslatePayload, config: Dict[str, Any]) -> Dict[str, str]:
    client = translate.Client()
    # The target language for translation
    target_language = payload.locale

    # Translates the text into the target language.
    translation = client.translate(payload.welcome_message, target_language=target_language)

    return {
        "original_text": payload.welcome_message,
        "translated_text": translation["translatedText"],
        "detected_source_language": translation["detectedSourceLanguage"],
    }
