import requests

def translate_onboarding_copy(text, locale, config):
    response = requests.post('https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=' + locale,
        headers={'Ocp-Apim-Subscription-Key': config['translator_key'], 'Ocp-Apim-Subscription-Region': config['translator_region']},
        json=[{'text': text}], timeout=30)
    response.raise_for_status()
    return response.json()[0]['translations'][0]['text']