from deepl import Translator
import os

def invoice_note_translate(text: str, target_lang: str = "EN") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        return "Error: Missing DEEPL_AUTH_KEY"
    try:
        translator = Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except Exception as e:
        return f"Error: {str(e)}"