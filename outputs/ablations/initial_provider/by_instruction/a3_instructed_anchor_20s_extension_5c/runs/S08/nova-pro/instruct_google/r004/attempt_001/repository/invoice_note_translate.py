from google.cloud import translate_v2 as translate

def translate_invoice_note(note, target_language='en'):
    client = translate.Client()
    translation = client.translate(note, target_language=target_language)
    return translation['translatedText']