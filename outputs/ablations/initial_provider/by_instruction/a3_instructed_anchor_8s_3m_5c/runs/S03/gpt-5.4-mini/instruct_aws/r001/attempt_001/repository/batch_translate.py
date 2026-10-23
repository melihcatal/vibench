from translation_client import get_translation_client
from translation_models import normalize_text_list


def batch_translate_texts(texts, source_language_code: str, target_language_code: str):
    client = get_translation_client()
    normalized = normalize_text_list(texts)
    return client.batch_translate_text(normalized, source_language_code, target_language_code)
