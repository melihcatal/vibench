import requests


def translate_onboarding_copy(text, locale):
    response = requests.post('https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=' + locale,
        headers={'Ocp-Apim-Subscription-Key': os.getenv('TRANSLATOR_KEY'), 'Ocp-Apim-Subscription-Region': os.getenv('TRANSLATOR_REGION')},
        json=[{'text': text}])
    response.raise_for_status()
    return response.json()[0]['translations'][0]['text']