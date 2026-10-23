import os
import requests
import uuid

def translate_text(text: str, target_language: str = "es") -> str:
    translator_key = os.environ.get("AZURE_TRANSLATOR_KEY")
    translator_region = os.environ.get("AZURE_TRANSLATOR_REGION")
    translator_endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")

    if not translator_key or not translator_region:
        raise ValueError("Please set AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION environment variables.")

    path = '/translate'
    constructed_url = translator_endpoint + path

    params = {
        'api-version': '3.0',
        'to': target_language
    }

    headers = {
        'Ocp-Apim-Subscription-Key': translator_key,
        'Ocp-Apim-Subscription-Region': translator_region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    if request.status_code == 200 and response and len(response) > 0 and 'translations' in response[0]:
        return response[0]['translations'][0]['text']
    else:
        print(f"Translation error: {response}")
        return f"[Translation Failed: {text}]"

if __name__ == "__main__":
    # Example usage (in a real scenario, this would receive live captions)
    sample_caption = "Hello world, how are you today?"
    translated_caption = translate_text(sample_caption, "fr")
    print(f"Original: {sample_caption}")
    print(f"Translated (fr): {translated_caption}")

    sample_caption_2 = "This is a test of the emergency broadcast system."
    translated_caption_2 = translate_text(sample_caption_2, "de")
    print(f"Original: {sample_caption_2}")
    print(f"Translated (de): {translated_caption_2}")
