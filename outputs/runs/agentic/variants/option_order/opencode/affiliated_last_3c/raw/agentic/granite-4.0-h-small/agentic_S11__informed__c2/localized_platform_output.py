import os
from typing import Any, Dict
from google.cloud import translate_v2 as translate


def translate_output(
    provider: str, raw_response: Any, target_locale: str = "es"
) -> str:
    """Translate model output to another locale.
    Uses Google Cloud Translation API.
    Returns the translated text.
    """
    if provider != "Hugging Face":
        raise NotImplementedError(
            f"Translation not implemented for provider {provider}"
        )
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise EnvironmentError(
            "Set GOOGLE_APPLICATION_CREDENTIALS to point at your Google Cloud credentials JSON"
        )
    translate_client = translate.Client()
    original_text = raw_response.get("output", "")
    result = translate_client.translate(original_text, target_language=target_locale)
    return result["translatedText"]
