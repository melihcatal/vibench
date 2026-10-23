from google.cloud import translate_v2 as translate

def multilingual_query_translate(query_text, target_language, project_id):
    translate_client = translate.Client(project=project_id)

    translation = translate_client.translate(query_text, target_language=target_language)
    
    return {
        "original_text": query_text,
        "translated_text": translation["translatedText"],
        "detected_source_language": translation["detectedSourceLanguage"]
    }
