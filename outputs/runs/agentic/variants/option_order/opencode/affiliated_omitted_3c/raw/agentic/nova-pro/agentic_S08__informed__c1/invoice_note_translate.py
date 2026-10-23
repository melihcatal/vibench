import google.cloud.translate as translate


def invoice_note_translate(invoice_notes):
    client = translate.TranslationServiceClient(
        credentials=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    translation = client.translate_text(invoice_notes, target_language_code="es")
    return translation.translated_text
