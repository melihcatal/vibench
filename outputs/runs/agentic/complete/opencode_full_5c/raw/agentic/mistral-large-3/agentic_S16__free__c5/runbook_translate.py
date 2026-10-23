from google.cloud import translate_v2 as translate
from typing import Dict, Any
import os


def runbook_translate(
    secret_response: SecretResponse, target_language: str = "es"
) -> Dict[str, Any]:
    translate_client = translate.Client()

    text_parts = []
    if secret_response.notes:
        text_parts.append(secret_response.notes)

    if secret_response.labels:
        text_parts.append(
            "Labels: "
            + ", ".join([f"{k}={v}" for k, v in secret_response.labels.items()])
        )

    combined_text = " | ".join(text_parts)
    if not combined_text:
        return {
            "secret_id": secret_response.secret_id,
            "version_id": secret_response.version_id,
            "translated_text": None,
            "target_language": target_language,
            "provider": "google-cloud-translate",
        }

    result = translate_client.translate(combined_text, target_language=target_language)

    return {
        "secret_id": secret_response.secret_id,
        "version_id": secret_response.version_id,
        "original_text": combined_text,
        "translated_text": result["translatedText"],
        "target_language": target_language,
        "provider": "google-cloud-translate",
    }
