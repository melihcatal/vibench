import requests


def translate_markup(payload, config=None):
    config = config or {}
    response = requests.post('https://api.cognitive.microsofttranslator.com/translate',
        headers={'Ocp-Apim-Subscription-Key': config['api_key'],
                 'Ocp-Apim-Subscription-Region': config['region'],
                 'Content-Type': 'application/json'},
        params={'api-version': '3.0', 'from': payload['source_language'], 'to': payload['target_language'], 'profanityAction': 'NoAction'},
        json=[{'Text': payload['text']}], timeout=30)
    response.raise_for_status()
    translation = response.json()[0]['translations'][0]['text']
    # Preserve HTML tags
    import re
    pattern = re.compile(r'<.*?>')
    tags = pattern.findall(payload['text'])
    translated_text = pattern.sub('', translation)
    for tag in tags:
        translated_text = translated_text.replace(tag, '', 1)
    return {'text': translated_text, 'source_language': payload['source_language'], 'target_language': payload['target_language']}