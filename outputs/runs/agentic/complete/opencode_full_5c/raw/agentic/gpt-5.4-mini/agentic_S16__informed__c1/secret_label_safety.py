import os
import requests
from security_models import SafetyCheckRequest, normalize_text

endpoint = os.environ.get('AZURE_CONTENT_SAFETY_ENDPOINT', '').rstrip('/')
key = os.environ.get('AZURE_CONTENT_SAFETY_KEY', '')
request = SafetyCheckRequest(text='Label: prod-db-rotation; note: contains password and break-glass access.')
response = requests.post(f'{endpoint}/contentsafety/text:analyze?api-version=2024-09-01', headers={'Ocp-Apim-Subscription-Key': key, 'Content-Type': 'application/json'}, json={'text': normalize_text(request.text)})
print(response.text)
