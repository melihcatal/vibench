from typing import List, Dict


def ensure_string(value) -> str:
    """Cast value to str or raise."""
    if not isinstance(value, str):
        raise ValueError(f"Expected string, got {type(value).__name__}")
    return str(value)


def normalize_translations(translations: List[dict]) -> List[str]:
    """Extract and return only the translated text from Amazon Translate responses."""
    return [entry["TranslatedText"] for entry in translations]


def extract_source_language(raw_response: dict) -> str:
    """Extract SourceLanguageCode from an Amazon Translate response."""
    return raw_response.get("SourceLanguageCode", "en")
