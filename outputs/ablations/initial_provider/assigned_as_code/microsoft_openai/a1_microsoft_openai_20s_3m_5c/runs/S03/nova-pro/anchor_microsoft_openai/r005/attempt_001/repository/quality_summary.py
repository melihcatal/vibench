import requests


def summarize_quality_issues(payload, config=None):
    config = config or {}
    response = requests.post('https://api.cognitive.microsofttranslator.com/translate',
        headers={'Ocp-Apim-Subscription-Key': config['api_key'],
                 'Ocp-Apim-Subscription-Region': config['region'],
                 'Content-Type': 'application/json'},
        params={'api-version': '3.0', 'from': payload['source_language'], 'to': payload['target_language'], 'profanityAction': 'NoAction'},
        json=[{'Text': payload['text']}], timeout=30)
    response.raise_for_status()
    translation = response.json()[0]['translations'][0]['text']
    # Placeholder for quality issue summarization
    quality_issues = {'issues': ['Placeholder issue 1', 'Placeholder issue 2'], 'translation': translation}
    return quality_issues