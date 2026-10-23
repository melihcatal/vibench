import requests


def quality_summary(translations):
    quality_issues = {}
    for translation in translations:
        response = requests.post('https://api.cognitive.microsofttranslator.com/translate',
            headers={'Ocp-Apim-Subscription-Key': os.getenv('MICROSOFT_TRANSLATOR_API_KEY'),
                     'Ocp-Apim-Subscription-Region': os.getenv('MICROSOFT_TRANSLATOR_REGION'),},
            params={'api-version': '3.0', 'from': translation['source_language'], 'to': translation['target_language'], 'profanityAction': 'NoAction'},
            json=[{'Text': translation['text']}], timeout=30)
        response.raise_for_status()
        quality_issues[translation['text']] = response.json()[0]['translations'][0]['detectedLanguage']['language']
    return quality_issues