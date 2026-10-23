from typing import Dict, Any
from google.cloud import translate_v2 as translate


def translate_invoice_note(text: str, target_language: str = "es") -> str:
    client = translate.Client.from_service_account_json(
        "google-translate-credentials.json"
    )

    result = client.translate(
        text,
        target_language=target_language,
        model="nmt",
    )

    return result["translatedText"]