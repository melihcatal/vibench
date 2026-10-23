import os
import requests
from typing import Optional
from identity_client import IdentityConfig
from identity_models import TranslationRequest, TranslationResponse


def translate_welcome_text(
    text: str, target_lang: str, source_lang: Optional[str] = None
) -> dict:
    """
    Translate onboarding copy into the user's locale using DeepL API.
    """
    config = IdentityConfig()

    if not config.deepl_api_key:
        raise ValueError("DeepL API key not configured")

    try:
        # DeepL API endpoint
        url = f"{config.deepl_api_url}/translate"

        # Prepare request payload
        payload = {
            "text": [text],
            "target_lang": target_lang.upper(),
            "auth_key": config.deepl_api_key,
        }

        if source_lang:
            payload["source_lang"] = source_lang.upper()

        # Make API request
        response = requests.post(url, data=payload)
        response.raise_for_status()

        result = response.json()

        if "translations" not in result or not result["translations"]:
            raise Exception("No translation returned from DeepL API")

        translation = result["translations"][0]

        return {
            "translated_text": translation["text"],
            "source_lang": translation.get(
                "detected_source_language", source_lang or "auto"
            ),
            "target_lang": target_lang,
            "detected_source_lang": translation.get("detected_source_language"),
            "provider": "DeepL",
        }

    except requests.exceptions.RequestException as e:
        print(f"DeepL API request error: {e}")
        raise
    except Exception as e:
        print(f"Translation error: {e}")
        raise
