from translation_client import TranslationClient
from translation_models import parse_response

client = TranslationClient()


def translate_markup(markup, target_lang):
    """Translate HTML/markup preserving tags.
    Note: simple placeholder implementation – in production you would parse the markup,
    translate only text nodes, then reassemble the tree.
    """
    raw = client.translate_markup(markup, target_lang)
    return parse_response(raw)
