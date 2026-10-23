import os
from deepl import DeepL


class TranslationClient:
    """Local helper to configure and use DeepL translation service."""

    def __init__(self):
        # Read auth key from environment (DEEPL_AUTH_KEY)
        auth_key = os.getenv("DEEPL_AUTH_KEY")
        if not auth_key:
            raise RuntimeError("DEEPL_AUTH_KEY environment variable not set")
        self.client = DeepL(auth_key=auth_key)

    def translate(
        self, text: str, source_lang: str = "EN", target_lang: str = "FR"
    ) -> Any:
        return self.client.translate_text(
            text, source_lang=source_lang, target_lang=target_lang
        )

    def translate_batch(
        self, texts: list[str], source_lang: str = "EN", target_lang: str = "FR"
    ) -> list[Any]:
        return self.client.translate_document(texts, source_lang, target_lang)

    def translate_html(
        self, markup: str, source_lang: str = "EN", target_lang: str = "FR"
    ) -> str:
        # DeepL SDK does not directly support HTML; split by tags and translate text nodes
        # Placeholder implementation – real integration should handle HTML tags properly
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(markup, "html.parser")
        for text in soup.find_all(text=True):
            if text.parent.name not in ["script", "style"]:
                translated = self.client.translate_text(text, source_lang, target_lang)
                text.replace_with(translated.translated_text)
        return str(soup)
