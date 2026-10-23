import os
from openai import OpenAI
from model_client import get_client


def translate_text(
    text: str, target_language: str = "Spanish", source_language: str = "English"
) -> str:
    """
    Translate generated model output using DeepL API.
    """
    import requests

    deepl_api_key = os.getenv("DEEPL_API_KEY")
    if not deepl_api_key:
        raise ValueError(
            "DEEPL_API_KEY environment variable is required for translation"
        )

    # Map language names to DeepL language codes
    language_codes = {
        "Spanish": "ES",
        "French": "FR",
        "German": "DE",
        "Italian": "IT",
        "Portuguese": "PT",
        "Russian": "RU",
        "Japanese": "JA",
        "Chinese": "ZH",
        "Korean": "KO",
        "Arabic": "AR",
        "Dutch": "NL",
        "Polish": "PL",
        "Swedish": "SV",
        "Turkish": "TR",
        "Hindi": "HI",
    }

    target_code = language_codes.get(target_language, "ES")

    try:
        response = requests.post(
            "https://api-free.deepl.com/v2/translate",
            headers={
                "Authorization": f"DeepL-Auth-Key {deepl_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "text": [text],
                "target_lang": target_code,
                "source_lang": language_codes.get(source_language, "EN"),
            },
            timeout=30,
        )

        response.raise_for_status()
        result = response.json()

        if "translations" in result and len(result["translations"]) > 0:
            return result["translations"][0]["text"]
        else:
            raise Exception("No translation returned from DeepL API")

    except requests.exceptions.RequestException as e:
        raise Exception(f"Translation API request failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to translate text: {str(e)}")
