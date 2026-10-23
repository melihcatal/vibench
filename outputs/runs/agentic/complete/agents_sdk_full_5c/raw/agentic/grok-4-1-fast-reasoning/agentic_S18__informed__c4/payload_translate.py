import os
from deepl import Translator
from typing import Dict, Any

def translate_message_payload(message: Dict[str, Any], target_lang: str = "ES") -> Dict[str, Any]:
    text = message.get("data", {}).get("payload", {}).get("text", "")
    if not text:
        return message
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    translated = message.copy()
    translated["data"] = translated["data"].copy()
    translated["data"]["payload"] = translated["data"]["payload"].copy()
    translated["data"]["payload"]["text"] = result.text
    return translated