import os
import requests

AZURE_TRANSLATOR_ENDPOINT = os.getenv('AZURE_TRANSLATOR_ENDPOINT')
AZURE_TRANSLATOR_KEY = os.getenv('AZURE_TRANSLATOR_KEY')

def translate_text(text, to_language):
    url = f'{AZURE_TRANSLATOR_ENDPOINT}/translate?api-version=3.0&to={to_language}'
    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_TRANSLATOR_KEY,
        'Content-Type': 'application/json',
    }
    payload = [{ 'text': text }]
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

if __name__ == '__main__':\n    text = 'This is a sample log message.'
    translation = translate_text(text, 'es')
    print(json.dumps(translation, indent=2))
