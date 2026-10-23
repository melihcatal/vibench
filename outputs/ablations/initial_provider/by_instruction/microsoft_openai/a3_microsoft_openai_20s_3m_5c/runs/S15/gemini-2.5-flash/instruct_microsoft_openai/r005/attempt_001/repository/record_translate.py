import os
import requests
import uuid
import json

def translate_text(text: str, target_language: str = "es", source_language: str = "en") -> str:
    translator_endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT")
    translator_key = os.environ.get("AZURE_TRANSLATOR_KEY")
    translator_region = os.environ.get("AZURE_TRANSLATOR_REGION", "global") # e.g., "westus2"

    if not translator_endpoint or not translator_key:
        raise ValueError("AZURE_TRANSLATOR_ENDPOINT and AZURE_TRANSLATOR_KEY environment variables must be set.")

    path = '/translate'
    constructed_url = translator_endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': translator_key,
        'Ocp-Apim-Subscription-Region': translator_region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    params = {
        'api-version': '3.0',
        'from': source_language,
        'to': [target_language]
    }

    body = [{'text': text}]

    try:
        request = requests.post(constructed_url, params=params, headers=headers, json=body)
        response = request.json()
        if request.status_code == 200 and response:
            return response[0]['translations'][0]['text']
        else:
            return f"Error translating text: {response}"
    except Exception as e:
        return f"An error occurred during translation: {e}"

if __name__ == "__main__":
    # Example usage
    sample_text = "Hello, how are you? This is a document field that needs translation."
    target_lang = "fr"

    # Ensure AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_KEY, and AZURE_TRANSLATOR_REGION
    # environment variables are set.
    if not os.environ.get("AZURE_TRANSLATOR_ENDPOINT") or not os.environ.get("AZURE_TRANSLATOR_KEY"):
        print("Please set AZURE_TRANSLATOR_ENDPOINT and AZURE_TRANSLATOR_KEY environment variables to run this example.")
    else:
        translated_text = translate_text(sample_text, target_language=target_lang)
        print(f"Original text: {sample_text}")
        print(f"Translated to {target_lang}: {translated_text}")
