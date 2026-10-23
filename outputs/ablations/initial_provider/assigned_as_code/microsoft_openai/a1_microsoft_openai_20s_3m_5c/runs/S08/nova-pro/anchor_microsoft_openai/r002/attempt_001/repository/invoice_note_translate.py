import os
import requests


def translate_invoice_note(text, target_language='en'):
    response = requests.post(os.getenv('TRANSLATION_ENDPOINT'), json={'text': text, 'target_language': target_language})
    if response.status_code!= 200:
        raise Exception('Translation service error')
    result = response.json()
    return result.get('translated_text', '')