# appeal_translate.py
"""Translate appeal text into review-friendly language using Azure Cognitive Services Translator.
"""
import os
from azure.ai.translation import TranslationClient
from safety_models import SafetyResponse

def translate_appeal(appeal_text: str, target_lang: str = "en") -> str:
    """Translate appeal text for reviewer consumption.
    This demonstration uses Azure Translator and prepends a note about original moderation context."""
    endpoint = "https://api.cognitive.microsofttranslator.com/"
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    if not key:
        raise RuntimeError("AZURE_TRANSLATOR_KEY environment variable not set")
    client = TranslationClient(endpoint=endpoint, credential=key)
    # Simple translation call (using latest SDK)
    result = client.translate(text=appeal_text, target_language=target_lang)
    translated = result.translated_text
    # Optionally prepend moderation context -- omitted for brevity
    return translated
