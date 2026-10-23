from google.cloud import translate_v2 as translate
import os

def translate_log_message(text: str, target_language: str = "es") -> str:
    translate_client = translate.Client()
    
    if not text:
        return ""
    
    result = translate_client.translate(
        text, 
        target_language=target_language
    )
    
    return result["translatedText"]