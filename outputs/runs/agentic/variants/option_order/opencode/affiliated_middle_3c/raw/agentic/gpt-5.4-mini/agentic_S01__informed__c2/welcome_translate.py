from google.cloud import translate_v3 as translate


def welcome_translate(text: str, locale: str):
    client = translate.TranslationServiceClient()
    parent = f"projects/{client.project_path if hasattr(client, 'project_path') else ''}/locations/global"
    response = client.translate_text(contents=[text], target_language_code=locale, parent=parent, mime_type="text/plain")
    return response.translations[0].translated_text
