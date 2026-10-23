from google.cloud import translate_v2 as translate


def appeal_translate(payload, config=None):
    client = translate.Client(config['api_key'])
    result = client.translate(payload['text'], target_language='en')
    return {'translated_text': result['translatedText']}