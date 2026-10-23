from typing import Dict, List, Any

def normalize_translation_request(text: str, source_lang: str, target_lang: str) -> Dict[str, str]:
    """
    Normalizes a translation request into a standard format.
    """
    return {
        "Text": text,
        "SourceLanguageCode": source_lang,
        "TargetLanguageCode": target_lang
    }

def parse_translation_response(response: Dict[str, Any]) -> str:
    """
    Parses a translation response and extracts the translated text.
    """
    return response.get('TranslatedText', '')
