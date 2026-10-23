import os
from google.cloud import translate_v2 as translate
from dotenv import load_dotenv

load_dotenv()

# For authentication, set the GOOGLE_APPLICATION_CREDENTIALS environment variable
# to the path of your service account key file.
try:
    translate_client = translate.Client()
except Exception as e:
    print(f"Could not initialize Google Cloud Translate client: {e}")
    translate_client = None

def translate_welcome_message(text: str, target_language: str) -> str:
    """
    Translates a welcome message to the user's target language using Google Cloud Translate.
    """
    if not translate_client:
        raise ConnectionError("Google Cloud Translate client not initialized.")
    if not text:
        return ""

    result = translate_client.translate(
        text,
        target_language=target_language,
        source_language="en"
    )

    return result['translatedText']
