import os
import requests
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

def translate_text(text, target_language='en'):
    subscription_key = os.getenv('AZURE_TRANSLATOR_API_KEY')
    endpoint = os.getenv('AZURE_TRANSLATOR_ENDPOINT')
    location = os.getenv('AZURE_TRANSLATOR_LOCATION')
    path = '/translate'
    constructed_url = endpoint + path
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    body = {
        'to': [target_language],
        'body': [{'text': text}]
    }
    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()
    return response['translations'][0]['text']