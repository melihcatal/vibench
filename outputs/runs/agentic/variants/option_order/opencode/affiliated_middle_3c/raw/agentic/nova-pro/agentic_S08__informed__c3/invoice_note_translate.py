from google.cloud import translate


def translate_invoice_notes(invoice_notes):
    client = translate.TranslationServiceClient()
    result = client.translate_text(invoice_notes)
    return result
