from typing import Dict, Any
import deepl
from model_client import get_auth_headers

def translate_platform_output(text: str, target_lang: str) -> Dict[str, Any]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    
    result = translator.translate_text(text, target_lang=target_lang)
    
    return {
        "translated_text": result.text,
        "detected_source_language": result.detected_source_lang,
        "target_language": target_lang,
    }