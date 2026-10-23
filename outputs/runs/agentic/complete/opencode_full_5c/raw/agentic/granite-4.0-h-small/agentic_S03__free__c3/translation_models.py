from typing import Dict, Any


# Request model for a single translation
class TranslationRequest:
    def __init__(self, text: str, target_lang: str, source_lang: str = "auto") -> None:
        self.text = text
        self.target_lang = target_lang
        self.source_lang = source_lang


# Successful response from the provider
class TranslationResponse:
    def __init__(self, raw: Dict[str, Any]) -> None:
        self.source = raw.get("source_lang")
        self.target = raw.get("target_lang")
        # List of translated text segments (preserves order)
        self.translated = raw.get("text")
        # Optional confidence or quality fields
        self.confidence = raw.get("confidence")


# Normalized output used by higher‑level functions
# We keep a uniform dict format that maps original keys to translated values
NormalizedTranslation = Dict[str, str]
