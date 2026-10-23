from google.cloud import translate_v2 as translate

def translate_text(text_content: str, target_language: str):
    translate_client = translate.Client()

    result = translate_client.translate(text_content, target_language=target_language)

    return {"status": "success", "translated_text": result['translatedText'], "detected_source_language": result['detectedSourceLanguage']}