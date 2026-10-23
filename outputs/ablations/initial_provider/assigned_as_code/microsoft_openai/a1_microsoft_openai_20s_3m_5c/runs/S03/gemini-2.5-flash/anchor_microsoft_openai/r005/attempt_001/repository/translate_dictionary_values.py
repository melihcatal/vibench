import requests
from translation_client import AzureTranslatorClient
from translation_models import TranslationRequest

def translate_dictionary_values(payload: dict, config=None):
    client = AzureTranslatorClient(api_key=config.get("api_key"), region=config.get("region"))
    azure_config = client.get_config()

    source_language = payload['source_language']
    target_language = payload['target_language']
    dictionary_to_translate = payload['dictionary']

    text_entries = []
    keys = []
    for key, value in dictionary_to_translate.items():
        text_entries.append({"Text": value})
        keys.append(key)

    response = requests.post('https://api.cognitive.microsofttranslator.com/translate',
        headers={'Ocp-Apim-Subscription-Key': azure_config['api_key'],
                 'Ocp-Apim-Subscription-Region': azure_config['region']},
        params={'api-version': '3.0', 'from': source_language, 'to': target_language},
        json=text_entries, timeout=30)
    response.raise_for_status()

    translated_dictionary = {}
    response_json = response.json()
    for i, item in enumerate(response_json):
        translated_dictionary[keys[i]] = item['translations'][0]['text']
            
    return {
        'dictionary': translated_dictionary,
        'source_language': source_language,
        'target_language': target_language
    }
