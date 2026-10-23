# payload_translate.py
# LATER-STEP: Translate customer-facing text in event payloads

import os
import json
from typing import Optional
from messaging_models import Event, ErrorResponse

# Choose a translation service based on env variable
TRANSLATOR = os.getenv("TRANSLATOR_PROVIDER", "google")

# Stub imports for illustration (replace with actual SDKs in production)
if TRANSLATOR == "google":
    # Placeholder Google Cloud Translation client
    from .translation_providers import google_translate as translate_client
elif TRANSLATOR == "deepl":
    # Placeholder DeepL client
    from .translation_providers import deepl_client as translate_client
else:
    # Fallback dummy translator (no-op)
    def translate(text: str, target_lang: str) -> Optional[str]:
        return text

    translate_client = type("Dummy", (), {"translate": staticmethod(translate)})


def translate_payload(event: Event, target_lang: str = "es") -> Optional[dict]:
    """Translate the 'text' field inside event.data to the target language.

    Returns a dict with the translated text or an ErrorResponse on failure.
    """
    if not event.data.get("text"):
        return ErrorResponse(
            code="MISSING_TEXT",
            message="Event payload missing required field: text",
            details={"required": "text"},
        )
    try:
        translated = translate_client.translate(event.data["text"], target_lang)
        # Attach translation back to payload
        event.data["translated"] = translated
        return {"translated": translated}
    except Exception as exc:
        return ErrorResponse(
            code="TRANSLATION_ERROR",
            message="Failed to translate payload",
            details={"exception": str(exc), "targetLang": target_lang},
        )


# ---- Placeholder provider skeletons -----------------------------------------
# Replace the following with the actual SDK calls for each provider.
# Example skeleton for Google Cloud Translation (v1):
# class google_translate:
#     @staticmethod
#     def translate(text: str, target_lang: str) -> str:
#         from google.cloud import translate_v2 as translate
#         client = translate.Client()
#         result = client.translate(text, target_language=target_lang)
#         return result['translatedText']
#
# Example skeleton for DeepL (using requests):
# class deepl_client:
#     @staticmethod
#     def translate(text: str, target_lang: str) -> str:
#         import requests, base64
#         url = 'https://api.deepl.com/v2/translate'
#         payload = {
#             'auth_key': os.getenv('DEEPL_AUTH_KEY'),
#             'text': text,
#             'target_lang': target_lang
#         }
#         resp = requests.post(url, data=payload)
#         resp.raise_for_status()
#         return resp.json()['translations'][0]['text']

if __name__ == "__main__":
    # Demo using the dummy translator (no-op)
    evt = Event(
        event_id="demo-001",
        data={"text": "Hello world!"},
        timestamp="2025-08-01T12:00:00Z",
    )
    res = translate_payload(evt, target_lang="fr")
    print("Translation result:", res)
