import os
import requests
import uuid

def localized_platform_output(text: str, target_language: str = "es") -> dict:
    """
    Translates platform model output for another locale using Azure Cognitive Services Translator.
    """
    # Azure Translator API endpoint and key
    endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT")
    subscription_key = os.environ.get("AZURE_TRANSLATOR_KEY")
    region = os.environ.get("AZURE_TRANSLATOR_REGION") # e.g., "westus2"

    if not all([endpoint, subscription_key, region]):
        raise ValueError("AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_KEY, and AZURE_TRANSLATOR_REGION environment variables must be set.")

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
        'text': text
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    translated_text = response[0]['translations'][0]['text']
    return {"translated_text": translated_text, "source_language": response[0]['detectedLanguage']['language']}
