import os
import requests
import uuid

def translate_caption(text: str, target_language: str = "es") -> str:
    key = os.environ.get("AZURE_TRANSLATOR_KEY")
    region = os.environ.get("AZURE_TRANSLATOR_REGION")
    endpoint = "https://api.cognitive.microsofttranslator.com"

    if not key or not region:
        raise ValueError("AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION environment variables must be set.")

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'to': target_language
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': region,
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
            print(f"Error during translation: {response}")
            return ""
    except Exception as e:
        print(f"Exception during translation: {e}")
        return ""

# Example usage (for integration test):
# if __name__ == "__main__":
#     os.environ["AZURE_TRANSLATOR_KEY"] = "YOUR_AZURE_TRANSLATOR_KEY"
#     os.environ["AZURE_TRANSLATOR_REGION"] = "YOUR_AZURE_TRANSLATOR_REGION"
#     translated_text = translate_caption("Hello, how are you?", "fr")
#     print(f"Translated text: {translated_text}")
