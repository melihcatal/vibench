import requests


def translate_text(payload, config=None):
    config = config or {}
    response = requests.post('https://api.cognitive.microsofttranslator.com/translate',
        headers={'Ocp-Apim-Subscription-Key': config['api_key'],
                 'Ocp-Apim-Subscription-Region': config['region']},
        params={'api-version': '3.0', 'from': payload['source_language'], 'to': payload['target_language']},
        json=[{'Text': payload['text']}], timeout=30)
    response.raise_for_status()
    return {'text': response.json()[0]['translations'][0]['text'],
            'source_language': payload['source_language'], 'target_language': payload['target_language']}
