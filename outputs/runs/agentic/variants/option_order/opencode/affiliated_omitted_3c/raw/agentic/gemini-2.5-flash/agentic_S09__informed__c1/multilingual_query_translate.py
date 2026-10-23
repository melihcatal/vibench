import os
import requests
import uuid
from typing import List, Dict, Any


def translate_query(
    query: str, target_language: str, source_language: str = "en"
) -> str:
    """
    Translates a query to a target language using Azure AI Translator API.
    """
    key = os.environ.get("AZURE_TRANSLATOR_KEY")
    region = os.environ.get("AZURE_TRANSLATOR_REGION")
    endpoint = "https://api.cognitive.microsofttranslator.com"

    if not key or not region:
        raise ValueError(
            "AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION environment variables must be set."
        )

    path = "/translate"
    constructed_url = endpoint + path

    params = {"api-version": "3.0", "from": source_language, "to": [target_language]}

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }

    body = [{"text": query}]

    try:
        request = requests.post(
            constructed_url, params=params, headers=headers, json=body
        )
        response = request.json()
        if (
            request.status_code == 200
            and response
            and len(response) > 0
            and "translations" in response[0]
        ):
            return response[0]["translations"][0]["text"]
        else:
            print(
                f"Translation failed with status code {request.status_code}: {response}"
            )
            return query  # Return original query on failure
    except requests.exceptions.RequestException as e:
        print(f"Error translating query: {e}")
        raise
