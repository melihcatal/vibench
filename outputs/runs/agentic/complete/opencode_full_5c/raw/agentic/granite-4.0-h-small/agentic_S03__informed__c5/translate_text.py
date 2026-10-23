from translation_client import TranslationClient
from translation_models import parse_response

client = TranslationClient()


def translate(text, target_lang):
    """Translate a single string to the target language."""
    # Example: client.translate_text(text, target_lang) will use the configured provider
    raw = client.translate_text(text, target_lang)
    return parse_response(raw)
