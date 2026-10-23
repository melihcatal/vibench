from google.cloud import translate_v2 as translate
import os

def runbook_translate(text: str, target_language: str = "es") -> str:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_PATH")
    client = translate.Client()
    
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]