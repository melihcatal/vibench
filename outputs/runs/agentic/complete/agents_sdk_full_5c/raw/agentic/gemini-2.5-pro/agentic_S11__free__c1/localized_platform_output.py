import deepl
from model_client import DEEPL_API_KEY

def translate_text_deepl(text: str, target_lang: str = "DE") -> str:
    """
    Translates text to another language using the DeepL API.
    """
    if not DEEPL_API_KEY:
        raise ValueError("DEEPL_API_KEY environment variable not set.")
    
    # Provider-specific client class: deepl.Translator
    translator = deepl.Translator(DEEPL_API_KEY)
    
    result = translator.translate_text(text, target_lang=target_lang)
    
    return result.text
