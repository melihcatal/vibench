from typing import Optional, List, Dict, Any

# Type hints for translation helpers
class TranslationParams(Dict[str, Any]):
    pass

TranslationResult = str
BatchTranslationResult = List[str]
DictionaryTranslationResult = Dict[str, str]

def normalize_target_lang(lang: str) -> str:
    """Normalize language code for DeepL."""
    return lang.upper()
