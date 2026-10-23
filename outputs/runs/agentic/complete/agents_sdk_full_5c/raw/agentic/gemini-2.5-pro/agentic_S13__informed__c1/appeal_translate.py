import os
import deepl

def translate_appeal_text(text: str, target_lang: str = "EN-US") -> str:
    """
    Translates appeal text from its original language to a target language
    for review by a multilingual team.

    Args:
        text: The appeal text to be translated.
        target_lang: The target language code (e.g., "EN-US", "ES", "FR").
                     DeepL Free supports: "BG", "CS", "DA", "DE", "EL", "EN-GB", 
                     "EN-US", "ES", "ET", "FI", "FR", "HU", "ID", "IT", "JA",
                     "KO", "LT", "LV", "NB", "NL", "PL", "PT-BR", "PT-PT", "RO",
                     "RU", "SK", "SL", "SV", "TR", "UK", "ZH".

    Returns:
        The translated text.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except deepl.DeepLException as e:
        print(f"An error occurred during translation: {e}")
        raise
