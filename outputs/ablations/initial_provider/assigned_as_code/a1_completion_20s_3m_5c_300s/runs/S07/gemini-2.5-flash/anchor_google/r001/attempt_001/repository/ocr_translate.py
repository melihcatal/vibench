from google.cloud import translate_v2 as translate

def ocr_translate(text: str, target_language: str, project_id: str):
    client = translate.Client(project=project_id)
    result = client.translate(text, target_language=target_language)
    return {"translated_text": result["translatedText"], "detected_source_language": result["detectedSourceLanguage"]}
