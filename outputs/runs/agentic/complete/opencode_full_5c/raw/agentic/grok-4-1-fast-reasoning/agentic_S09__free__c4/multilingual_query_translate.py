from embeddings_client import get_deepl_translator


def multilingual_query_translate(query: str, target_lang: str = "EN") -> str:
    translator = get_deepl_translator()
    result = translator.translate_text(query, target_lang=target_lang)
    return result.text
