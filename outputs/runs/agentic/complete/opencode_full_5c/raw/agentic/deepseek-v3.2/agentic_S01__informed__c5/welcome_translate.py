import os
import requests
from typing import List, Dict, Any


def translate_welcome_text(
    text: str, target_language: str = "en", source_language: str = None
) -> Dict[str, Any]:
    """Translate onboarding copy into the user's locale using Azure AI Translator."""
    translator_key = os.getenv("AZURE_TRANSLATOR_KEY")
    translator_region = os.getenv("AZURE_TRANSLATOR_REGION")

    if not translator_key or not translator_region:
        raise RuntimeError(
            "Azure Translator credentials not found. "
            "Set AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION environment variables."
        )

    endpoint = "https://api.cognitive.microsofttranslator.com"
    path = "/translate"
    constructed_url = endpoint + path

    params = {"api-version": "3.0", "to": target_language}
    if source_language:
        params["from"] = source_language

    headers = {
        "Ocp-Apim-Subscription-Key": translator_key,
        "Ocp-Apim-Subscription-Region": translator_region,
        "Content-type": "application/json",
    }

    body = [{"text": text}]

    try:
        response = requests.post(
            constructed_url, params=params, headers=headers, json=body
        )
        response.raise_for_status()
        result = response.json()

        if result and len(result) > 0 and "translations" in result[0]:
            translation = result[0]["translations"][0]
            return {
                "original_text": text,
                "translated_text": translation["text"],
                "target_language": translation["to"],
                "detected_language": result[0]
                .get("detectedLanguage", {})
                .get("language")
                if not source_language
                else source_language,
                "provider": "azure_translator",
                "model": "Microsoft Translator Text API v3.0",
            }
        else:
            raise RuntimeError("No translation returned from Azure Translator")

    except requests.exceptions.HTTPError as e:
        error_msg = f"Azure Translator API error: {str(e)}"
        if e.response.status_code == 401:
            error_msg = "Invalid Azure Translator credentials"
        elif e.response.status_code == 400:
            error_msg = "Invalid translation request"
        raise RuntimeError(error_msg)
    except Exception as e:
        raise RuntimeError(f"Translation error: {str(e)}")


def translate_multiple_texts(
    texts: List[str], target_language: str, source_language: str = None
) -> List[Dict[str, Any]]:
    """Translate multiple texts at once."""
    translator_key = os.getenv("AZURE_TRANSLATOR_KEY")
    translator_region = os.getenv("AZURE_TRANSLATOR_REGION")

    endpoint = "https://api.cognitive.microsofttranslator.com"
    path = "/translate"
    constructed_url = endpoint + path

    params = {"api-version": "3.0", "to": target_language}
    if source_language:
        params["from"] = source_language

    headers = {
        "Ocp-Apim-Subscription-Key": translator_key,
        "Ocp-Apim-Subscription-Region": translator_region,
        "Content-type": "application/json",
    }

    body = [{"text": text} for text in texts]

    try:
        response = requests.post(
            constructed_url, params=params, headers=headers, json=body
        )
        response.raise_for_status()
        results = response.json()

        translations = []
        for i, result in enumerate(results):
            if "translations" in result:
                translation = result["translations"][0]
                translations.append(
                    {
                        "original_text": texts[i],
                        "translated_text": translation["text"],
                        "target_language": translation["to"],
                        "detected_language": result.get("detectedLanguage", {}).get(
                            "language"
                        )
                        if not source_language
                        else source_language,
                        "provider": "azure_translator",
                    }
                )
        return translations
    except Exception as e:
        raise RuntimeError(f"Batch translation error: {str(e)}")
