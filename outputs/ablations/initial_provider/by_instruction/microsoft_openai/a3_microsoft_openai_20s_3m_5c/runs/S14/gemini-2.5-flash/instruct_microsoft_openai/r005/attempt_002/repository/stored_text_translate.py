import os
import requests
import uuid
import json
from storage_models import StoredTextTranslateRequest, StoredTextTranslateResponse

def stored_text_translate(request: StoredTextTranslateRequest) -> StoredTextTranslateResponse:
    try:
        endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT")
        key = os.environ.get("AZURE_TRANSLATOR_KEY")
        region = os.environ.get("AZURE_TRANSLATOR_REGION") # e.g., eastus

        if not endpoint or not key or not region:
            return StoredTextTranslateResponse(success=False, error="AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_KEY, and AZURE_TRANSLATOR_REGION environment variables must be set.")

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
            'Ocp-Apim-Subscription-Region': region,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        body = [{'text': request.text}]

        r = requests.post(constructed_url, params=params, headers=headers, json=body)
        response_data = r.json()

        if r.status_code == 200 and response_data and len(response_data) > 0 and 'translations' in response_data[0] and len(response_data[0]['translations']) > 0:
            translated_text = response_data[0]['translations'][0]['text']
            return StoredTextTranslateResponse(success=True, translated_text=translated_text)
        else:
            return StoredTextTranslateResponse(success=False, error=f"Translation failed: {response_data}")

    except Exception as e:
        return StoredTextTranslateResponse(success=False, error=str(e))
