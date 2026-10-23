from security_models import TranslatedText
import os
import requests
import uuid
import json

def translate_compliance_note(text: str, target_language: str, source_language: str = "en") -> TranslatedText:
    """Translates encryption or compliance notes for reviewers using Azure Translator service."""
    # Azure Translator Text API Key and Endpoint
    key = os.environ.get("AZURE_TRANSLATOR_TEXT_KEY")
    endpoint = os.environ.get("AZURE_TRANSLATOR_TEXT_ENDPOINT")
    location = os.environ.get("AZURE_TRANSLATOR_TEXT_LOCATION") # Example: "westus2"

    if not key or not endpoint or not location:
        raise ValueError("Azure Translator Text API key, endpoint, or location not found in environment variables.")

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': source_language,
        'to': [target_language]
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text
    }]

    try:
        request = requests.post(constructed_url, params=params, headers=headers, json=body)
        request.raise_for_status() # Raise an exception for HTTP errors
        response = request.json()

        translated_text_content = response[0]['translations'][0]['text']

        return TranslatedText(
            source_language=source_language,
            target_language=target_language,
            text=text,
            translated_text=translated_text_content
        )
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error calling Azure Translator Text API: {e}") from e
    except (IndexError, KeyError) as e:
        raise RuntimeError(f"Unexpected response format from Azure Translator Text API: {e}, Response: {response}") from e

