from google.cloud import translate_v3 as translate


def runbook_translate(text: str, target_language_code: str = "es") -> str:
    client = translate.TranslationServiceClient()
    parent = "projects/placeholder/locations/global"
    response = client.translate_text(contents=[text], target_language_code=target_language_code, parent=parent)
    return response.translations[0].translated_text if response.translations else ""
