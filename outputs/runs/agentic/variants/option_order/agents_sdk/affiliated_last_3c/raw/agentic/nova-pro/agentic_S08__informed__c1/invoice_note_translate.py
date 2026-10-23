import os
import google.cloud.translate

translate_client = google.cloud.translate.Client()

def invoice_note_translate(text, target_language='en'):
    translation = translate_client.translate(text, target_language=target_language)
    return translation['translatedText']