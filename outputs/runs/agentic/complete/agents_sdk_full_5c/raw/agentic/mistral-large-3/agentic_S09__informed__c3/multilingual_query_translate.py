import os
from deepl import Translator


class QueryTranslator:
    """Translate queries for multilingual embedding search using DeepL."""

    def __init__(self):
        self.api_key = os.getenv("DEEPL_AUTH_KEY")
        if not self.api_key:
            raise ValueError("DEEPL_AUTH_KEY environment variable not set")
        self.translator = Translator(self.api_key)

    def translate(self, text: str, target_lang: str = "EN") -> str:
        result = self.translator.translate_text(text, target_lang=target_lang)
        return result.text


def translate_query(query: str, target_lang: str = "EN") -> str:
    return QueryTranslator().translate(query, target_lang)