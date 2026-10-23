import requests
import uuid
import os

def record_translate(text_content, to_language='en', from_language='auto'):
    endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT")
    key = os.environ.get("AZURE_TRANSLATOR_KEY")
    region = os.environ.get("AZURE_TRANSLATOR_REGION") # e.g., "global", "westus2"

    path = '/translate'
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    params = {
        'api-version': '3.0',
        'to': to_language,
    }
    if from_language != 'auto':
        params['from'] = from_language

    body = [{'text': text_content}]

    try:
        request = requests.post(constructed_url, params=params, headers=headers, json=body)
        response = request.json()
        
        if request.status_code == 200 and response and len(response) > 0 and 'translations' in response[0]:
            translated_text = response[0]['translations'][0]['text']
            detected_language = response[0].get('detectedLanguage', {}).get('language')
            return {'translated_text': translated_text, 'detected_language': detected_language}
        else:
            return {'translated_text': None, 'error': response}

    except Exception as e:
        print(f"Error translating text with Azure Translator: {e}")
        return {'translated_text': None, 'error': str(e)}
