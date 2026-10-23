import os
from google.cloud import translate_v2 as translate

def record_translate(text_content: str, target_language: str) -> str:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set. Using default credentials.")

    client = translate.Client()
    result = client.translate(text_content, target_language=target_language)
    return result['translatedText']
