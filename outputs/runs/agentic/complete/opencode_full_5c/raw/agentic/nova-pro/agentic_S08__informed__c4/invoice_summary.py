from google.cloud import translate


def invoice_summary(invoice_data):
    client = translate.TranslationServiceClient()
    parent = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/global"
    response = client.translate_text(parent, invoice_data, "en")
    return response.translations[0].translated_text
