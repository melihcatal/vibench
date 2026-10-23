import os
import requests

def localized_platform_output(text: str, target_language: str):
    url = f"https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to={target_language}"
    resp = requests.post(url, headers={'Ocp-Apim-Subscription-Key': os.environ['AZURE_TRANSLATOR_KEY'], 'Ocp-Apim-Subscription-Region': os.environ['AZURE_TRANSLATOR_REGION'], 'Content-Type': 'application/json'}, json=[{'text': text}], timeout=30)
    resp.raise_for_status()
    return resp.json()
