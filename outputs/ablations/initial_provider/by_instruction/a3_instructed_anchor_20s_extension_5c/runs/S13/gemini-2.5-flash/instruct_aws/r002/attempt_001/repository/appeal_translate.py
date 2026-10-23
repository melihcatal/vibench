import os
import requests
import json

def appeal_translate(text: str, target_lang: str = "en") -> dict:
    """
    Translate appeal text for review using DeepL API.
    """
    deepl_api_key = os.environ.get("DEEPL_API_KEY")
    deepl_api_url = os.environ.get("DEEPL_API_URL", "https://api-free.deepl.com/v2/translate")

    if not deepl_api_key:
        raise ValueError("DEEPL_API_KEY environment variable not set.")

    headers = {
        "Authorization": f"DeepL-Auth-Key {deepl_api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "text": [text],
        "target_lang": target_lang.upper()
    }

    try:
        response = requests.post(deepl_api_url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        translation_result = response.json()

        translated_text = translation_result["translations"][0]["text"]
        source_lang = translation_result["translations"][0]["detected_source_language"]

        return {
            "original_text": text,
            "translated_text": translated_text,
            "source_language": source_lang,
            "target_language": target_lang,
            "raw_deepl_response": translation_result
        }
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "message": "Failed to connect to DeepL API."}
