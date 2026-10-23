import os
from google.cloud import translate_v2 as translate
from security_models import EncryptionResponse, DecryptionResponse

def translate_compliance_note(text: str, target_language: str = "es") -> str:
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]