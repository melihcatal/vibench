from google.cloud import translate_v2 as translate

def translate_script(text: str, target_language: str, project_id: str) -> str:
    client = translate.Client(project=project_id)
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
