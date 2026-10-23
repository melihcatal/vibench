from.model_client import ModelClient

def translate_output(text, locale):
    client = ModelClient().get_client()
    result = client.translate(text, locale)
    return result