from google.cloud import translate_v2 as translate
import os

def translate_transcript(text: str, target_language: str = 'es'):
    # Before running, ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # pointing to your service account key file.
    # Example: os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/path/to/your/keyfile.json"

    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return result['translatedText']
