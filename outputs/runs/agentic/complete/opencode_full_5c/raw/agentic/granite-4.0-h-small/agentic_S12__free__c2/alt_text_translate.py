import os
from translate_client import translate_text


# Translate a short visual description into another language
def alt_text_translate(description: str, target_lang: str = "es") -> str:
    """Translate the generated description into the target language using a translation API.","""
    # Provider-specific: here we use Google Cloud Translation (or any chosen provider)
    api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_TRANSLATE_API_KEY not set")
    # Simple provider call placeholder
    translated = translate_text(description, target_lang)
    return translated


# Export for later step usage
__all__ = ["alt_text_translate"]
