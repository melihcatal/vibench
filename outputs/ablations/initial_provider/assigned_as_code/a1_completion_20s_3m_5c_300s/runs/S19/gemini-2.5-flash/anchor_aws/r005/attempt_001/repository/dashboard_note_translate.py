from google.cloud import translate_v2 as translate

def translate_dashboard_note(payload, project_id):
    client = translate.Client(project=project_id)

    text = payload["text"]
    target_language = payload["target_language"]

    result = client.translate(text, target_language=target_language)

    return {
        "original_text": text,
        "translated_text": result["translatedText"],
        "source_language": result["detectedSourceLanguage"],
        "target_language": target_language
    }
