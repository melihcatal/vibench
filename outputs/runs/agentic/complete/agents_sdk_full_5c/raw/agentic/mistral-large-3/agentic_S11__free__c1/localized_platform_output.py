from google.cloud import translate_v2 as translate
import os

def translate_output(text: str, target_language: str = "es") -> str:
    client = translate.Client.from_service_account_json(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]