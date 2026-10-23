import requests
import uuid

def translate_appeal_text(text: str, target_language: str, config: dict) -> str:
    path = '/translate'
    constructed_url = config['azure_translator_endpoint'] + path

    headers = {
        'Ocp-Apim-Subscription-Key': config['azure_translator_api_key'],
        'Ocp-Apim-Subscription-Region': config['azure_translator_region'],
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    params = {
        'api-version': config.get('azure_translator_api_version', '3.0'),
        'to': target_language
    }

    body = [{'text': text}]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    
    if response and isinstance(response, list) and 'translations' in response[0]:
        return response[0]['translations'][0]['text']
    return ""
