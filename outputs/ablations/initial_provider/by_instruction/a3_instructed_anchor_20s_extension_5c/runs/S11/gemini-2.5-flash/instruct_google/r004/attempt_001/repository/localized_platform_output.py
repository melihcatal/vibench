from google.cloud import translate_v2 as translate

def localized_platform_output(text_content: str, target_language: str):
    """Translates Google Vertex AI platform model output for another locale using Google Cloud Translation API."""
    translate_client = translate.Client()
    
    response = translate_client.translate(text_content, target_language=target_language)
    
    return {"original_text": text_content, "translated_text": response['translatedText'], "target_language": target_language}
