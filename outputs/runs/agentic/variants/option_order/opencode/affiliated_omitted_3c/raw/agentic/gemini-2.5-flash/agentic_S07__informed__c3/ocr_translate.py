from document_client import get_deepl_auth_key
from document_models import TranslatedText
import deepl


def translate_text(text: str, target_language: str = "en") -> TranslatedText:
    auth_key = get_deepl_auth_key()
    translator = deepl.Translator(auth_key)

    result = translator.translate_text(text, target_lang=target_language)

    return TranslatedText(
        original_text=text, translated_text=result.text, target_language=target_language
    )
