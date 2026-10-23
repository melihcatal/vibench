from google.cloud import translate_v2 as translate
import os

def translate_onboarding_copy(text, target_language_code):
    """
    Translates onboarding copy into the user's locale using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS.
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Target language must be provided
    if not target_language_code:
        raise ValueError("Target language code must be provided.")

    try:
        result = translate_client.translate(
            text, target_language=target_language_code
        )
        translated_text = result["translatedText"]
        return {"original_text": text, "translated_text": translated_text, "language": result["detectedSourceLanguage"]}
    except Exception as e:
        raise Exception(f"Google Cloud Translation failed: {e}")
