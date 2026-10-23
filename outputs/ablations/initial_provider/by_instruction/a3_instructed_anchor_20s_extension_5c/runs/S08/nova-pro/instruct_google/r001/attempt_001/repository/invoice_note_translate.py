from google.cloud import translate_v2 as translate

def translate_invoice_note(text, target_language='en'):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']