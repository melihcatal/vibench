import requests


def batch_translate(payloads, config=None):
    config = config or {}
    response = requests.post('https://api.cognitive.microsofttranslator.com/translate',
        headers={'Ocp-Apim-Subscription-Key': config['api_key'],
                 'Ocp-Apim-Subscription-Region': config['region'],
                 'Content-Type': 'application/json'},
        params={'api-version': '3.0', 'from': payloads[0]['source_language'], 'to': payloads[0]['target_language'], 'profanityAction': 'NoAction'},
        json=[{'Text': payload['text']} for payload in payloads], timeout=30)
    response.raise_for_status()
    translations = [{'text': result['translations'][0]['text'], 'source_language': payload['source_language'], 'target_language': payload['target_language']} for result, payload in zip(response.json(), payloads)]
    return translations