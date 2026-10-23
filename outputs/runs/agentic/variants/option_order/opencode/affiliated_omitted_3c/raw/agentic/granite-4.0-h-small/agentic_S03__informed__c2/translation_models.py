from typing import List, Dict, Any

# Generic request/response models for translation operations
# These structures are provider‑agnostic; concrete providers map to these fields.

# Request definition for a single‑string translation
TranslateRequest = Dict[str, Any]

# Minimal fields expected in a successful translation response
# Concrete implementations should fill these fields according to provider specs
TranslateResponse = Dict[str, Any]

# Example: Minimal fields for Alibaba Cloud Translation response
# Expected keys: "TargetText"
AlibabaTranslateRequest = Dict[str, Any]
AlibabaTranslateResponse = Dict[str, str]  # contains "TargetText"

# Example normalization helper – adapts provider‑specific response to a unified format


def normalize_translation_response(provider_response: Any) -> str:
    """Convert any provider's translation result to a plain string.

    Args:
        provider_response: Raw response from a translation SDK or REST call.

    Returns:
        The extracted translated text as a string.
    """
    # Alibaba Machine Translation example – raw response might be a dict
    if isinstance(provider_response, dict):
        return provider_response.get("TargetText", "")
    # If the response is already a string (e.g., REST call), return as‑is
    if isinstance(provider_response, str):
        return provider_response
    # Fallback – attempt to fetch a generic "text" key
    return getattr(provider_response, "text", "")


# Example usage placeholder – shows how a same‑scenario file could consume these helpers
# from translation_client import translate_with_alimt
# raw = translate_with_alimt("Hello")
# translated = normalize_translation_response(raw)

# Placeholder functions for other providers (to be filled later)
# def normalize_deepl_response(...): ...
# def normalize_google_response(...): ...
# def normalize_azure_response(...): ...
# def normalize_amazon_response(...): ...

# End of translation_models.py
