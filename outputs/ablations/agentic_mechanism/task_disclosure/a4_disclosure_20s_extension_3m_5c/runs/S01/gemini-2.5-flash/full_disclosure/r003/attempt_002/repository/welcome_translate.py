from google.cloud import translate_v2 as translate
import os

def translate_text(text: str, target_locale: str) -> str:
    """Translates text into the target locale using Google Cloud Translation API."""
    # Instantiates a client
    translate_client = translate.Client()

    # Set your Google Cloud Project ID as an environment variable or pass it directly
    # os.environ["GOOGLE_CLOUD_PROJECT"] = "your-gcp-project-id"

    response = translate_client.translate(
        text,
        target_language=target_locale
    )
    return response["translatedText"]
