
import os
import requests
import uuid

def translate_consent_text(text: str, target_language: str = "en", source_language: str = None) -> dict:
    # Azure Translator Text API endpoint
    translator_endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT")
    translator_key = os.environ.get("AZURE_TRANSLATOR_SUBSCRIPTION_KEY")
    translator_region = os.environ.get("AZURE_TRANSLATOR_REGION") # Required for multi-service/global resources

    if not translator_endpoint or not translator_key or not translator_region:
        raise ValueError("Azure Translator endpoint, subscription key, and region must be set in environment variables.")

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
        'to': target_language
    }
    if source_language:
        params['from'] = source_language

    body = [{'text': text}]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    response_status = request.status_code

    if response_status != 200:
        print(f"Error translating text: {response}")
        request.raise_for_status()

    translated_texts = []
    for translation in response:
        for t in translation.get('translations', []):
            translated_texts.append(t.get('text'))
    
    print(f"Original text: '{text}'")
    print(f"Translated text ({target_language}): '{translated_texts[0] if translated_texts else ''}'")

    return {"original_text": text, "translated_text": translated_texts[0] if translated_texts else "", "target_language": target_language}

if __name__ == '__main__':
    # Example usage: Set your Azure Translator credentials
    # os.environ['AZURE_TRANSLATOR_ENDPOINT'] = "https://api.cognitive.microsofttranslator.com/"
    # os.environ['AZURE_TRANSLATOR_SUBSCRIPTION_KEY'] = 'YOUR_TRANSLATOR_KEY'
    # os.environ['AZURE_TRANSLATOR_REGION'] = 'YOUR_TRANSLATOR_REGION'

    consent_copy_german = "Ich stimme der Verarbeitung meiner Daten gemäß der Datenschutzerklärung zu."
    consent_copy_spanish = "Acepto el procesamiento de mis datos de acuerdo con la política de privacidad."

    if os.environ.get("AZURE_TRANSLATOR_ENDPOINT") and os.environ.get("AZURE_TRANSLATOR_SUBSCRIPTION_KEY") and os.environ.get("AZURE_TRANSLATOR_REGION"):
        print("\n--- Translating German consent to English ---")
        translate_consent_text(consent_copy_german, target_language="en", source_language="de")

        print("\n--- Translating Spanish consent to French ---")
        translate_consent_text(consent_copy_spanish, target_language="fr", source_language="es")
    else:
        print("Please set AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_SUBSCRIPTION_KEY, and AZURE_TRANSLATOR_REGION environment variables to run this example.")

