import deepl

DEEPL_AUTH_KEY = 'your_deepl_auth_key'

def translate_invoice_note(note_text):
    client = deepl.Client(auth_key=DEEPL_AUTH_KEY)
    response = client.translate_text(note_text, target_lang='EN-US')
    # Extract translated text from response
    return translated_text