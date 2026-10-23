import os
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account

def translate_stored_text(text: str, target_language: str = "en") -> str:
    # Google Cloud Translation client setup
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable must be set.")

    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    translate_client = translate.Client(credentials=credentials)

    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']
