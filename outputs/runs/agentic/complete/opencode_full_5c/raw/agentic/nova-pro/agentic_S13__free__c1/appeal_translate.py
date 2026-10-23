import safety_client


def translate_appeal(text):
    client = safety_client.get_client()
    translated_text = client.translate_text(text)
    return translated_text
