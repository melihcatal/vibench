import os
from google.cloud import translate_v2 as translate
from typing import Dict, Any, Optional
from safety_models import TranslationRequest, TranslationResult

def appeal_translate(request: TranslationRequest, config: Dict[str, Any] = None) -> TranslationResult:
    config = config or {}
    # Google Cloud credentials are typically handled via GOOGLE_APPLICATION_CREDENTIALS
    # or default service account. For simplicity, we assume the environment is set up.
    # No explicit API key is usually passed for Google Cloud client libraries once gcloud is configured.
    # If an API key is needed for a specific setup, it would be passed to the client.

    client = translate.Client()

    # Target language is required
    if not request.target_language:
        raise ValueError("Target language must be specified for translation.")

    translation = client.translate(
        request.text,
        target_language=request.target_language,
        source_language=request.source_language # Optional
    )

    translated_text = translation['translatedText']
    return TranslationResult(translated_text=translated_text)
