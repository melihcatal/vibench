from google.cloud import translate_v3 as translate

from security_client import load_config


def runbook_translate(text: str, target_language_code: str = "es"):
    config = load_config()
    client = translate.TranslationServiceClient()
    parent = f"projects/{config.project_id}/locations/global"
    response = client.translate_text(request={"parent": parent, "contents": [text], "mime_type": "text/plain", "target_language_code": target_language_code})
    return response.translations[0].translated_text
