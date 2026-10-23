import json
from typing import Dict, Any, Optional
from model_models import ModelInvocationResponse

# Placeholder localization dictionary (could be loaded from .po/.json files)
TRANSLATIONS = {
    "en": {
        "hello": "Hello",
        "goodbye": "Goodbye",
    },
    "es": {
        "hello": "Hola",
        "goodbye": "Adiós",
    },
    "fr": {
        "hello": "Bonjour",
        "goodbye": "Au revoir",
    },
}


def translate_output(
    response: ModelInvocationResponse, target_locale: str = "es"
) -> ModelInvocationResponse:
    """Translates plain‑text model output into another locale.

    Args:
        response: The original invocation response.
        target_locale: Locale code (e.g., "es", "fr").

    Returns:
        A new response with translated text and updated metadata.
    """
    # Only translate when output is a simple string
    original_text = response.output
    if not isinstance(original_text, str):
        # Non‑string output: leave unchanged but note locale switch
        return ModelInvocationResponse(
            output=original_text,
            metadata={**response.metadata, "locale": target_locale},
        )
    original_text_lower = original_text.lower()
    translated = TRANSLATIONS.get(target_locale, {}).get(
        original_text_lower, original_text
    )
    # Preserve original metadata and add locale info
    updated_meta = response.metadata.copy()
    updated_meta["locale"] = target_locale
    return ModelInvocationResponse(
        output=translated,
        metadata=updated_meta,
    )
