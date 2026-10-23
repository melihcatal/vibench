import google.cloud.translate as translate


def invoice_summary(invoice_fields):
    client = translate.TranslationServiceClient()
    parent = f"projects/{os.environ['GOOGLE_PROJECT_ID']}"
    text = f"Vendor: {invoice_fields['vendor']}, Date: {invoice_fields['date']}, Total: {invoice_fields['total']}"
    response = client.translate_text(
        parent=parent, contents=[text], target_language_code="en"
    )
    return response.translations[0].translated_text
