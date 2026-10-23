import os
import requests
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

def embed_text(text):
    subscription_key = os.getenv('AZURE_TEXT_EMBEDDING_API_KEY')
    endpoint = os.getenv('AZURE_TEXT_EMBEDDING_ENDPOINT')
    path = '/embeddings'
    constructed_url = endpoint + path
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-type': 'application/json'
    }
    body = {
        'input': text
    }
    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()
    return response['data'][0]['embedding']