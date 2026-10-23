from google.cloud import translate_v2 as translate
import os

def translate_welcome_message(text: str, target_language: str):
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authentication is handled appropriately for Google Cloud.
    # For local development, you might set it to the path of your service account key file.
    # Example: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    translate_client = translate.Client()

    # Translate the text
    result = translate_client.translate(text, target_language=target_language)

    return result['translatedText']
