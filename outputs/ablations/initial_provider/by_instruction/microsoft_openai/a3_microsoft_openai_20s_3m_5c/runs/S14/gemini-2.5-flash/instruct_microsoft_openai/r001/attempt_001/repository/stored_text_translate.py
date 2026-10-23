import os
import requests
import uuid
from dotenv import load_dotenv
from storage_models import StoredTextTranslateRequest, StoredTextTranslateResponse

load_dotenv()

def stored_text_translate(request: StoredTextTranslateRequest) -> StoredTextTranslateResponse:
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
    location = os.getenv("AZURE_TRANSLATOR_LOCATION")

    if not key or not endpoint or not location:
        return StoredTextTranslateResponse(success=False, error="Azure Translator environment variables (KEY, ENDPOINT, LOCATION) not set.")

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'to': request.target_language
    }
    if request.source_language:
        params['from'] = request.source_language

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': request.text}]

    try:
        translator_response = requests.post(constructed_url, params=params, headers=headers, json=body)
        translator_response.raise_for_status() # Raise an exception for HTTP errors
        response_json = translator_response.json()

        if response_json and len(response_json) > 0 and 'translations' in response_json[0] and len(response_json[0]['translations']) > 0:
            translated_text = response_json[0]['translations'][0]['text']
            return StoredTextTranslateResponse(success=True, translated_text=translated_text)
        else:
            return StoredTextTranslateResponse(success=False, error="Translation failed: No translations found in the response.")

    except requests.exceptions.RequestException as e:
        return StoredTextTranslateResponse(success=False, error=f"Translation request failed: {e}")
    except Exception as e:
        return StoredTextTranslateResponse(success=False, error=str(e))
