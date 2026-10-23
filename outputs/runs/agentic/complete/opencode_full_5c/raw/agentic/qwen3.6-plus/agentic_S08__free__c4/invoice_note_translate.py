import os
import json
import requests
from typing import Dict, Any, List, Optional
from document_client import get_azure_translator_config


AZURE_TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com/"
AZURE_TRANSLATOR_API_VERSION = "3.0"


def translate_invoice_note(
    text: str, target_language: str = "en", source_language: Optional[str] = None
) -> Dict[str, Any]:
    config = get_azure_translator_config()
    subscription_key = config["subscription_key"]
    region = config.get("region", "global")
    endpoint = config.get("endpoint", AZURE_TRANSLATOR_ENDPOINT).rstrip("/")

    translate_url = f"{endpoint}/translate?api-version={AZURE_TRANSLATOR_API_VERSION}&to={target_language}"

    if source_language:
        translate_url += f"&from={source_language}"

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json",
    }

    body = [{"text": text}]

    response = requests.post(translate_url, headers=headers, json=body)
    response.raise_for_status()

    result = response.json()
    return parse_translation_response(result, text, target_language, source_language)


def translate_invoice_notes_batch(
    notes: List[str], target_language: str = "en", source_language: Optional[str] = None
) -> List[Dict[str, Any]]:
    config = get_azure_translator_config()
    subscription_key = config["subscription_key"]
    region = config.get("region", "global")
    endpoint = config.get("endpoint", AZURE_TRANSLATOR_ENDPOINT).rstrip("/")

    translate_url = f"{endpoint}/translate?api-version={AZURE_TRANSLATOR_API_VERSION}&to={target_language}"

    if source_language:
        translate_url += f"&from={source_language}"

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json",
    }

    body = [{"text": note} for note in notes]

    response = requests.post(translate_url, headers=headers, json=body)
    response.raise_for_status()

    results = response.json()
    translations = []

    for idx, (result, original_note) in enumerate(zip(results, notes)):
        translations.append(
            parse_translation_response(
                [result], original_note, target_language, source_language
            )
        )

    return translations


def translate_invoice_description(
    vendor_name: str,
    description: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
) -> Dict[str, Any]:
    translation_result = translate_invoice_note(
        text=description,
        target_language=target_language,
        source_language=source_language,
    )

    return {
        "vendor_name": vendor_name,
        "original_description": description,
        "translated_description": translation_result["translated_text"],
        "source_language": translation_result["detected_language"],
        "target_language": target_language,
        "translation_confidence": translation_result.get("confidence", 1.0),
        "translation_service": "azure-translator",
    }


def parse_translation_response(
    result: List[Dict[str, Any]],
    original_text: str,
    target_language: str,
    source_language: Optional[str],
) -> Dict[str, Any]:
    if not result:
        return {
            "original_text": original_text,
            "translated_text": original_text,
            "detected_language": source_language or "unknown",
            "target_language": target_language,
            "confidence": 0.0,
        }

    first_result = result[0]
    translations = first_result.get("translations", [])
    translated_text = (
        translations[0].get("text", original_text) if translations else original_text
    )

    detected_language = source_language
    confidence = 1.0

    if "detectedLanguage" in first_result:
        detected_language = first_result["detectedLanguage"].get(
            "language", source_language or "unknown"
        )
        confidence = first_result["detectedLanguage"].get("score", 1.0)

    return {
        "original_text": original_text,
        "translated_text": translated_text,
        "detected_language": detected_language,
        "target_language": target_language,
        "confidence": confidence,
        "translation_endpoint": AZURE_TRANSLATOR_ENDPOINT,
    }


if __name__ == "__main__":
    sample_note = "Facture pour fournitures de bureau - Livraison urgente"
    result = translate_invoice_note(sample_note, target_language="en")
    print(json.dumps(result, indent=2))
