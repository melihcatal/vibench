from typing import Dict, Any, Optional
import os
from google.cloud import translate_v2 as translate


def translate_invoice_note(text: str, target_language: str = "en") -> Optional[str]:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translation API.
    """
    if not text:
        return None

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("Missing Google Cloud Project ID environment variable.")

    client = translate.Client()
    result = client.translate(text, target_language=target_language)

    return result["translatedText"]
