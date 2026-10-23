from google.cloud import translate


def invoice_note_translate(note, target_language):
    client = translate.TranslationServiceClient()
    parent = "projects/YOUR_PROJECT_ID/locations/global"
    response = client.translate_text(
        parent=parent, contents=[note], target_language_code=target_language
    )
    return response.translations[0].translated_text
