from google.cloud import translate_v2 as translate


def alt_text_translate(payload, config=None):
    client = translate.Client()
    translation = client.translate(payload['description'], target_language=config['target_language'])
    return {'translated_description': translation['translatedText']}