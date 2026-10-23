import os
import requests
from speech_client import get_deepl_api_key
from speech_models import TranslationRequest, TranslationResult

DEEPL_API_BASE_URL = "https://api-free.deepl.com/v2/translate"

def translate_script(request: TranslationRequest) -> TranslationResult:
    api_key = get_deepl_api_key()

    headers = {
        "Authorization": f"DeepL-Auth-Key {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "text": [request.text],
        "source_lang": request.source_lang.upper(),
        "target_lang": request.target_lang.upper(),
    }

    try:
        response = requests.post(DEEPL_API_BASE_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if "translations" in data and data["translations"]:
            translated_text = data["translations"][0]["text"]
            return TranslationResult(
                translated_text=translated_text,
                source_lang=request.source_lang,
                target_lang=request.target_lang
            )
        else:
            raise RuntimeError(f"DeepL API returned no translations: {data}")

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"DeepL API request failed: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during DeepL translation: {e}")
