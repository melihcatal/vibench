from translation_client import TranslationClient
from translation_models import parse_response

client = TranslationClient()


def batch_translate(texts, target_lang):
    """Translate a list of strings while preserving order."""
    results = []
    for txt in texts:
        raw = client.translate_text(txt, target_lang)
        results.append(parse_response(raw))
    return results
