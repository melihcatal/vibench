from google.cloud import translate_v2 as translate
import os

def translate_welcome_message(text: str, target_language: str = "es") -> dict:
    """
    Translates onboarding copy into the user's locale using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    translate_client = translate.Client()

    try:
        result = translate_client.translate(
            text,
            target_language=target_language
        )
        return {
            "original_text": text,
            "translated_text": result["translatedText"],
            "source_language": result["detectedSourceLanguage"],
            "target_language": target_language,
            "message": "Text translated successfully."
        }
    except Exception as e:
        return {"error": str(e)}
