import os
import requests
import uuid

def runbook_translate(payload, config=None):
    config = config or {}
    text_to_translate = payload.get('text', '')
    target_language = payload.get('target_language', 'en')

    if not text_to_translate:
        return {'translated_text': '', 'message': 'No text provided for translation.'}

    # Azure Translator Text API configuration
    # Ensure these environment variables are set:
    # AZURE_TRANSLATOR_TEXT_ENDPOINT, AZURE_TRANSLATOR_TEXT_SUBSCRIPTION_KEY, AZURE_TRANSLATOR_TEXT_REGION
    endpoint = os.environ.get("AZURE_TRANSLATOR_TEXT_ENDPOINT") or config.get('azure_translator_text_endpoint')
    subscription_key = os.environ.get("AZURE_TRANSLATOR_TEXT_SUBSCRIPTION_KEY") or config.get('azure_translator_text_subscription_key')
    region = os.environ.get("AZURE_TRANSLATOR_TEXT_REGION") or config.get('azure_translator_text_region')

    if not all([endpoint, subscription_key, region]):
        return {'translated_text': '', 'message': 'Azure Translator Text API configuration missing.'}

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'to': target_language
    }

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text_to_translate
    }]

    try:
        request = requests.post(constructed_url, params=params, headers=headers, json=body)
        response = request.json()
        
        if request.status_code == 200 and response and len(response) > 0 and 'translations' in response[0]:
            translated_text = response[0]['translations'][0]['text']
            return {'translated_text': translated_text, 'message': 'Text translated successfully.'}
        else:
            return {'translated_text': '', 'message': f'Error during translation: {response.get('error', {}).get('message', 'Unknown error')}'}
    except Exception as e:
        return {'translated_text': '', 'message': f'Exception during translation: {str(e)}'}
