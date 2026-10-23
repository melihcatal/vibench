from google.cloud import translate_v2 as translate
import os

def translate_text(text: str, target_language: str = "en") -> str:
    """
    Translates generated model output using Google Cloud Translation.
    Expects GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set. "
              "Google Cloud Translation might not authenticate correctly.")

    translate_client = translate.Client()

    result = translate_client.translate(
        text,
        target_language=target_language
    )
    return result["translatedText"]
