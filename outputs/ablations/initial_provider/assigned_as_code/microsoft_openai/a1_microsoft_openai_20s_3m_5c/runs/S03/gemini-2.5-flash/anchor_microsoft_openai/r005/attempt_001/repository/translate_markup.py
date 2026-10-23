import requests
from translation_client import AzureTranslatorClient
from translation_models import TranslationRequest, TranslationResponse

def translate_markup(payload: TranslationRequest, config=None):
    client = AzureTranslatorClient(api_key=config.get("api_key"), region=config.get("region"))
    azure_config = client.get_config()

    response = requests.post('https://api.cognitive.microsofttranslator.com/translate',
        headers={'Ocp-Apim-Subscription-Key': azure_config['api_key'],
                 'Ocp-Apim-Subscription-Region': azure_config['region']},
        params={'api-version': '3.0', 'from': payload.source_language, 'to': payload.target_language, 'textType': 'html'},
        json=[{'Text': payload.text}], timeout=30)
    response.raise_for_status()

    translated_text = response.json()[0]['translations'][0]['text']
            
    return TranslationResponse(
        text=translated_text,
        source_language=payload.source_language,
        target_language=payload.target_language
    )
