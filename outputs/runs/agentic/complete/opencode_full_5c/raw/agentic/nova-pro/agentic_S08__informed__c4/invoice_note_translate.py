from google.cloud import translate


def invoice_note_translate(invoice_note):
    client = translate.TranslationServiceClient()
    parent = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/global"
    response = client.translate_text(parent, invoice_note, "en")
    return response.translations[0].translated_text
