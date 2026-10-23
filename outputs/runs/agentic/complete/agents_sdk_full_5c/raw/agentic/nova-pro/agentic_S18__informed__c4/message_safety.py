import os
import requests

os.environ['AZURE_CONTENT_SAFETY_ENDPOINT'] = 'your-azure-content-safety-endpoint'
os.environ['AZURE_CONTENT_SAFETY_KEY'] = 'your-azure-content-safety-key'

def check_message_safety(message):
    url = f"{os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')}/contentsafety/v1.0/screen?api-version=2023-07-01-preview"
    headers = {'Ocp-Apim-Subscription-Key': os.getenv('AZURE_CONTENT_SAFETY_KEY'), 'Content-Type': 'application/json'}
    payload = {'text': message}
    response = requests.post(url, headers=headers, json=payload)
    return response.json()