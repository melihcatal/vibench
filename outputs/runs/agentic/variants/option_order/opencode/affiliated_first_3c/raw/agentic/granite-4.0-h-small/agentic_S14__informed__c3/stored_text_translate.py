import os
from storage_models import TranslateRequest, TranslateResponse
from typing import Any

PROVIDER = "Google Cloud Translation"

# Placeholder translation client using Google Cloud Translation SDK
# In production you would import google-cloud-translate and instantiate translate_client
try:
    from google.cloud import translate_v2 as translate
except ImportError:
    translate = None  # placeholder

# Initialize client once
if translate:
    # Assumes GOOGLE_APPLICATION_CREDENTIALS env var is set elsewhere
    translation_client = translate.Client()
else:
    translation_client = None


def translate_text(request: TranslateRequest) -> TranslateResponse:
    """
    Translate extracted document text to the target language.

    Args:
        request (TranslateRequest): source text and target language code.
    Returns:
        TranslateResponse: translated text.
    """
    if not translation_client:
        raise RuntimeError(
            f"[{PROVIDER}] Translation client not initialized - missing credentials"
        )
    result = translation_client.translate(
        request.source_text, target_language=request.target_language
    )
    # The SDK returns a dict with 'translatedText'; extract it
    translated = result.get("translatedText", "")
    print(
        f"[{PROVIDER}] Translated {len(translated)} characters to {request.target_language}"
    )
    return TranslateResponse(translated_text=translated)


# Simple CLI wrapper
if __name__ == "__main__":
    import sys, json

    if len(sys.argv) != 3:
        print(
            "Usage: stored_text_translate.py <source_text> <target_language (e.g., 'es')>"
        )
        sys.exit(1)
    src = sys.argv[1]
    tgt = sys.argv[2]
    resp = translate_text(TranslateRequest(source_text=src, target_language=tgt))
    print(
        json.dumps(
            {"translated_text": resp.translated_text}, ensure_ascii=False, indent=2
        )
    )
