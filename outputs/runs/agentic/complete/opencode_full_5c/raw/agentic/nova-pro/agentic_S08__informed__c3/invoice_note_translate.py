import deepl


def translate_invoice_notes(text):
    client = deepl.Client("your-auth-key")
    response = client.translate_text(text, target_lang="EN-US")
    return response.text
