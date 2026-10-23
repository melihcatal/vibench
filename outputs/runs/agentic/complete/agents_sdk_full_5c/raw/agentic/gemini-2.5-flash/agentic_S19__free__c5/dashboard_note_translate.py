from google.cloud import translate_v2 as translate

def translate_dashboard_note(text: str, target_language_code: str, project_id: str):
    client = translate.Client(project=project_id) # Provider-identifying signal: translate.Client

    result = client.translate(text, target_language=target_language_code)

    return {
        "original_text": result["input"],
        "translated_text": result["translatedText"],
        "source_language": result["detectedSourceLanguage"],
        "target_language": target_language_code,
    }
