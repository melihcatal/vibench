SUPPORTED_DEEPL_LANGS = ["BG", "CS", "DA", "DE", "EL", "EN", "EN-GB", "EN-US", "ES", "ET", "FI", "FR", "HU", "IT", "JA", "LT", "LV", "NB", "NL", "PL", "PT", "PT-BR", "PT-PT", "RO", "RU", "SK", "SL", "SV", "ZH"]

def validate_deepl_lang(lang: str) -> str:
    """
    Validate and normalize language code for DeepL.
    """
    normalized = lang.replace("-", "").upper()
    if not normalized or normalized not in SUPPORTED_DEEPL_LANGS:
        raise ValueError(f"Unsupported DeepL language code: {lang}. Supported: {SUPPORTED_DEEPL_LANGS}")
    return normalized
