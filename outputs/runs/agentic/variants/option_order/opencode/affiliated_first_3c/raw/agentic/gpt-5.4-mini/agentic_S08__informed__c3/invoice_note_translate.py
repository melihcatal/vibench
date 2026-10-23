from deepl import Translator


def invoice_note_translate(text: str, target_lang: str = "EN") -> str:
    translator = Translator()
    return translator.translate_text(text, target_lang=target_lang).text
