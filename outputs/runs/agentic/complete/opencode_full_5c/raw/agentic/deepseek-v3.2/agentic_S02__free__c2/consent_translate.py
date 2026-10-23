import os
import requests
from typing import Dict, Any
from identity_models import TranslationRequest, TranslationResponse


def translate_consent(request: TranslationRequest) -> TranslationResponse:
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable is required")

    params = {
        "auth_key": api_key,
        "text": request.text,
        "target_lang": request.target_language.upper(),
    }

    if request.source_language:
        params["source_lang"] = request.source_language.upper()

    response = requests.post("https://api-free.deepl.com/v2/translate", data=params)
    response.raise_for_status()

    result = response.json()
    translation = result["translations"][0]

    return TranslationResponse(
        translated_text=translation["text"],
        source_language=translation.get(
            "detected_source_language", request.source_language or ""
        ),
        target_language=request.target_language,
        provider="deepl",
    )
