from deepl import Translator

from document_client import require_env


def invoice_note_translate(text: str, target_lang: str = "EN-US") -> str:
    translator = Translator(require_env("DEEPL_AUTH_KEY"))
    return translator.translate_text(text, target_lang=target_lang).text
