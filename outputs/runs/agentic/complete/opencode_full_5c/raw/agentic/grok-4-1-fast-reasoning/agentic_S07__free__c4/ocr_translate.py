import deepl
from document_client import DEEPL_AUTH_KEY


def ocr_translate(text: str, target_lang: str = "EN") -> dict:
    translator = deepl.Translator(DEEPL_AUTH_KEY)
    result = translator.translate_text(text, target_lang=target_lang)
    return {"original": text, "translated": result.text, "target_lang": target_lang}
