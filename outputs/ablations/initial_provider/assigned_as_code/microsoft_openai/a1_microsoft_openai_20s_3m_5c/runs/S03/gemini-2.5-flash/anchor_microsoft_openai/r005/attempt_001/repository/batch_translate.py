import requests
from translation_client import AzureTranslatorClient
from translation_models import BatchTranslationRequest, BatchTranslationResponse

def batch_translate(payload: BatchTranslationRequest, config=None):
    client = AzureTranslatorClient(api_key=config.get("api_key"), region=config.get("region"))
    azure_config = client.get_config()

    text_entries = []
    for text in payload.texts:
        text_entries.append({"Text": text})

    response = requests.post('https://api.cognitive.microsofttranslator.com/translate',
        headers={'Ocp-Apim-Subscription-Key': azure_config['api_key'],
                 'Ocp-Apim-Subscription-Region': azure_config['region']},
        params={'api-version': '3.0', 'from': payload.source_language, 'to': payload.target_language},
        json=text_entries, timeout=30)
    response.raise_for_status()

    translated_texts = []
    for item in response.json():
        for translation in item['translations']:
            translated_texts.append(translation['text'])
            
    return BatchTranslationResponse(
        translations=translated_texts,
        source_language=payload.source_language,
        target_language=payload.target_language
    )
