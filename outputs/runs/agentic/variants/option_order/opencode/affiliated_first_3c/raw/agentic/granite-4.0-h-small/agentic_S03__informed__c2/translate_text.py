import deepl
from translation_client import TranslationClient


def translate_text(source_text: str, target_lang: str = "EN") -> str:
    """Translate a single text string using DeepL SDK."""
    client = TranslationClient()
    result = client.translate_text(source_text, target_lang=target_lang)
    return result


if __name__ == "__main__":
    print(translate_text("Bonjour"))
