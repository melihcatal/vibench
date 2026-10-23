import requests


def translate_dictionary_values(payload, config=None):
    config = config or {}
    translated_values = {}
    for key, value in payload.items():
        response = requests.post('https://api.cognitive.microsofttranslator.com/translate',
            headers={'Ocp-Apim-Subscription-Key': config['api_key'],
                     'Ocp-Apim-Subscription-Region': config['region'],
                     'Content-Type': 'application/json'},
            params={'api-version': '3.0', 'from': payload['source_language'], 'to': payload['target_language'], 'profanityAction': 'NoAction'},
            json=[{'Text': value}], timeout=30)
        response.raise_for_status()
        translated_values[key] = response.json()[0]['translations'][0]['text']
    return {'dictionary': translated_values, 'source_language': payload['source_language'], 'target_language': payload['target_language']}