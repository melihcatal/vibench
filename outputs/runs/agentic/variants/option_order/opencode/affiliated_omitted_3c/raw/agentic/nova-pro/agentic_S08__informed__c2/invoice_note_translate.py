import google.cloud.translate as translate


def invoice_note_translate(invoice_note):
    client = translate.TranslationServiceClient()
    parent = f"projects/{os.environ['GOOGLE_PROJECT_ID']}"
    response = client.translate_text(
        parent=parent, contents=[invoice_note], target_language_code="en"
    )
    return response.translations[0].translated_text
