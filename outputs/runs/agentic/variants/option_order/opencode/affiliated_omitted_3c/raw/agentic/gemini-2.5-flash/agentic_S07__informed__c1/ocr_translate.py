import requests
import json
import uuid  # Required for X-ClientTraceId
from document_client import get_azure_translator_credentials
from document_models import TextExtractionResult, TranslationResult


def translate_text(
    text_to_translate: TextExtractionResult, target_language: str
) -> TranslationResult:
    credentials = get_azure_translator_credentials()
    endpoint = credentials["endpoint"]
    key = credentials["key"]
    region = credentials["region"]

    path = "/translate"
    constructed_url = endpoint + path

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }

    params = {"api-version": "3.0", "to": target_language}

    body = [{"text": text_to_translate.text_content}]

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
            translated_text = response[0]["translations"][0]["text"]
            source_language = response[0].get("detectedLanguage", {}).get("language")
            return TranslationResult(
                translated_text=translated_text,
                source_language=source_language,
                target_language=target_language,
            )
        else:
            raise Exception(f"Translation failed: {response}")

    except requests.exceptions.RequestException as e:
        raise Exception(f"Network or request error during translation: {e}")
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse JSON response from translator service: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred during translation: {e}")
