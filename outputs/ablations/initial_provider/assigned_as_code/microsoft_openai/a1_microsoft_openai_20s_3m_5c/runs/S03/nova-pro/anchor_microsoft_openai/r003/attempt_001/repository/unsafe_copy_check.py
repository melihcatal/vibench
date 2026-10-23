import requests


def unsafe_copy_check(translation):
    response = requests.post('https://api.cognitive.microsofttranslator.com/moderate',
        headers={'Ocp-Apim-Subscription-Key': os.getenv('MICROSOFT_TRANSLATOR_API_KEY'),
                 'Ocp-Apim-Subscription-Region': os.getenv('MICROSOFT_TRANSLATOR_REGION'),},
        params={'api-version': '3.0', 'autocorrect': 'true'},
        json=[{'Text': translation['text']}], timeout=30)
    response.raise_for_status()
    return response.json()[0]['moderated'] == 'true'