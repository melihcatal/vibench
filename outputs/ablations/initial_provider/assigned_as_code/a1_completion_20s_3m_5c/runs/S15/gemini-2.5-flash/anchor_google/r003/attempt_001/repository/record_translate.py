from google.cloud import translate_v2 as translate
import os

def record_translate(payload, config=None):
    config = config or {}
    translate_client = translate.Client()
    
    text_to_translate = payload["document_content"]
    target_language = payload.get("target_language", "es")  # Default to Spanish
    
    result = translate_client.translate(text_to_translate, target_language=target_language)
    
    return {"translated_text": result["translatedText"], "original_language": result["detectedSourceLanguage"]}
