import deepl


def translate_invoice_notes(invoice_notes):
    client = deepl.Client(api_key=os.getenv("DEEPL_AUTH_KEY"))
    result = client.translate_text(invoice_notes, target_lang="EN-US")
    return result.text
