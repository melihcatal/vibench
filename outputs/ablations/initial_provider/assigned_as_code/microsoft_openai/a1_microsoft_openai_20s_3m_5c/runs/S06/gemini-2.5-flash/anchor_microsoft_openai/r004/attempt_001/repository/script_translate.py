from google.cloud import translate_v2 as translate

def translate_script(text: str, target_language: str, project_id: str) -> dict:
    client = translate.Client(project=project_id)
    
    result = client.translate(text, target_language=target_language)
    
    return {
        "translated_text": result['translatedText'],
        "original_text": result['input'],
        "source_language": result['detectedSourceLanguage']
    }
