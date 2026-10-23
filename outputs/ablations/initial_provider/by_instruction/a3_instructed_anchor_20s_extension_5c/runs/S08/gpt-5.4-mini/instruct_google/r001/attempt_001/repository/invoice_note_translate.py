from google.cloud import translate_v3


def invoice_note_translate(text: str, target_language: str = "en") -> str:
    client = translate_v3.TranslationServiceClient()
    parent = client.location_path("PROJECT_ID", "global")
    response = client.translate_text(contents=[text], target_language_code=target_language, parent=parent)
    return response.translations[0].translated_text if response.translations else text
