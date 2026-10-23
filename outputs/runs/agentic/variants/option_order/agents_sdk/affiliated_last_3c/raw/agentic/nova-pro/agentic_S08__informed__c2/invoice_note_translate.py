from google.cloud import translate

def translate_invoice_note(text):
    client = translate.TranslationServiceClient()
    # Add code to translate the invoice note