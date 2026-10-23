import os
from google.cloud import translate_v2 as translate
from dotenv import load_dotenv

load_dotenv()

def translate_onboarding_message(text: str, target_locale: str) -> str:
    """
    Translates onboarding copy into the user's locale using Google Cloud Translate.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set in the environment.
    """
    # This provider is identifiable by the 'google.cloud.translate_v2' import and client.
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_locale)
    
    return result["translatedText"]
