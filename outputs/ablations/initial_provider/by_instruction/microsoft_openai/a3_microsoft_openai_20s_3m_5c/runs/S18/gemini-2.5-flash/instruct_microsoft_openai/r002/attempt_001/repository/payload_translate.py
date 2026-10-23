import os
import requests
import uuid

def translate_text(text: str, target_language: str = "es") -> str:
    """
    Translates the given text using Azure Translator Text API.
    """
    key = os.environ.get("AZURE_TRANSLATOR_TEXT_KEY")
    endpoint = os.environ.get("AZURE_TRANSLATOR_TEXT_ENDPOINT")
    location = os.environ.get("AZURE_TRANSLATOR_TEXT_LOCATION") # e.g., "global", "eastus"

    if not all([key, endpoint, location]):
        raise ValueError("AZURE_TRANSLATOR_TEXT_KEY, AZURE_TRANSLATOR_TEXT_ENDPOINT, and AZURE_TRANSLATOR_TEXT_LOCATION environment variables must be set.")

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'to': target_language
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': text}]

    try:
        request = requests.post(constructed_url, params=params, headers=headers, json=body)
        response = request.json()
        if request.status_code == 200 and response and len(response) > 0 and 'translations' in response[0]:
            return response[0]['translations'][0]['text']
        else:
            print(f"Azure Translator API error: {response}")
            return f"Translation failed: {text}"
    except Exception as e:
        print(f"Error calling Azure Translator Text API: {e}")
        return f"Translation failed: {text}"

if __name__ == "__main__":
    # Example usage
    text_to_translate = "Hello, how are you?"
    translated_text = translate_text(text_to_translate, "fr")
    print(f"Original: {text_to_translate}\nTranslated (French): {translated_text}")

    text_to_translate_es = "Thank you for your order."
    translated_text_es = translate_text(text_to_translate_es, "es")
    print(f"Original: {text_to_translate_es}\nTranslated (Spanish): {translated_text_es}")
