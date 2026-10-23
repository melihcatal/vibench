from googletrans import Translator

def translate(text: str, target_lang: str = 'en') -> str:
    """Translate text to target language using googletrans library."""
    translator = Translator()
    result = translator.translate(text, dest=target_lang)
    return result.text
