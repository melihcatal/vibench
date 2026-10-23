import os

try:
    from deepl import DeepL  # Using DeepL as example provider
except ImportError:
    raise ImportError("Install DeepL SDK: pip install deepl")

# Load API key from environment (DeepL)
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
if not DEEPL_AUTH_KEY:
    raise RuntimeError("Set the DEEPL_AUTH_KEY environment variable")


class TranslationClient:
    """Wrapper around DeepL SDK providing helper methods for text translation."""

    def __init__(self):
        self.client = DeepL(auth_key=DEEPL_AUTH_KEY)

    def translate(
        self, text: str, source_lang: str = "EN", target_lang: str = "FR"
    ) -> str:
        """Translate a single string."""
        result = self.client.translate(
            text=text, source_lang=source_lang, target_lang=target_lang
        )
        return result["text"]

    def batch_translate(
        self, texts: list[str], source_lang: str = "EN", target_lang: str = "FR"
    ) -> list[str]:
        """Translate a list of strings while preserving order."""
        batch = self.client.translate_batch(
            texts, source_lang=source_lang, target_lang=target_lang
        )
        return [item["text"] for item in batch]
