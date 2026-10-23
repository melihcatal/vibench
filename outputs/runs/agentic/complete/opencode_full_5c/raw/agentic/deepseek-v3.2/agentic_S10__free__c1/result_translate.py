import os
from typing import Optional
from openai import OpenAI
from model_client import get_client
from model_models import TaskType


def translate_text(
    text: str, target_language: str, source_language: Optional[str] = None
) -> str:
    """
    Translate generated model output using DeepL API.

    Args:
        text: Text to translate
        target_language: Target language code (e.g., 'EN', 'ES', 'FR', 'DE')
        source_language: Source language code (optional, auto-detected if None)

    Returns:
        Translated text
    """
    import requests

    # Get DeepL API key from environment
    deepl_api_key = os.getenv("DEEPL_API_KEY")
    if not deepl_api_key:
        raise ValueError("DEEPL_API_KEY environment variable must be set")

    # DeepL API endpoint
    deepl_url = "https://api-free.deepl.com/v2/translate"

    # Prepare request parameters
    params = {"auth_key": deepl_api_key, "text": text, "target_lang": target_language}

    if source_language:
        params["source_lang"] = source_language

    try:
        response = requests.post(deepl_url, data=params)
        response.raise_for_status()

        result = response.json()

        if "translations" in result and len(result["translations"]) > 0:
            translated_text = result["translations"][0]["text"]
            detected_source_lang = result["translations"][0].get(
                "detected_source_language", source_language
            )

            return translated_text
        else:
            raise Exception("No translation returned from DeepL API")

    except requests.exceptions.RequestException as e:
        # Fallback to OpenAI translation if DeepL fails
        return translate_with_openai(text, target_language, source_language)
    except Exception as e:
        raise Exception(f"Failed to translate text: {str(e)}")


def translate_with_openai(
    text: str, target_language: str, source_language: Optional[str] = None
) -> str:
    """
    Fallback translation using OpenAI.

    Args:
        text: Text to translate
        target_language: Target language
        source_language: Source language

    Returns:
        Translated text
    """
    client = get_client()

    language_names = {
        "EN": "English",
        "ES": "Spanish",
        "FR": "French",
        "DE": "German",
        "IT": "Italian",
        "PT": "Portuguese",
        "RU": "Russian",
        "ZH": "Chinese",
        "JA": "Japanese",
        "KO": "Korean",
    }

    target_lang_name = language_names.get(target_language.upper(), target_language)
    source_lang_name = (
        language_names.get(source_language.upper(), source_language)
        if source_language
        else "the detected language"
    )

    prompt = f"""Translate the following text from {source_lang_name} to {target_lang_name}:

{text}

Translation:"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a professional translator. Translate text accurately to {target_lang_name}.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=len(text) * 2,
        )

        translation = response.choices[0].message.content.strip()
        return translation

    except Exception as e:
        raise Exception(f"Failed to translate with OpenAI: {str(e)}")


def detect_language(text: str) -> str:
    """
    Detect the language of text using DeepL API.

    Args:
        text: Text to analyze

    Returns:
        Detected language code
    """
    import requests

    deepl_api_key = os.getenv("DEEPL_API_KEY")
    if not deepl_api_key:
        raise ValueError("DEEPL_API_KEY environment variable must be set")

    deepl_url = "https://api-free.deepl.com/v2/translate"

    params = {
        "auth_key": deepl_api_key,
        "text": text[:100],  # Only need first 100 chars for detection
        "target_lang": "EN",  # Any target language works for detection
    }

    try:
        response = requests.post(deepl_url, data=params)
        response.raise_for_status()

        result = response.json()

        if "translations" in result and len(result["translations"]) > 0:
            detected_lang = result["translations"][0].get(
                "detected_source_language", "EN"
            )
            return detected_lang
        else:
            return "EN"  # Default to English

    except Exception:
        # Fallback to simple detection
        return "EN"
