import os
import deepl


def translate_queries(
    queries: list[str],
    target_lang: str = "EN",
    source_lang: str = None,
    auth_key: str = None,
) -> list[str]:
    auth_key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is not set")
    translator = deepl.Translator(auth_key)
    source_lang_kw = {}
    if source_lang:
        source_lang_kw["source_lang"] = source_lang
    translated = []
    for query in queries:
        result = translator.translate_text(
            query, target_lang=target_lang, **source_lang_kw
        )
        translated.append(result.text)
    return translated


def translate_and_prepare_for_multilingual_search(
    queries: list[str],
    documents: list[str],
    target_lang: str = "EN",
    source_lang: str = None,
) -> dict:
    translated_queries = translate_queries(
        queries, target_lang=target_lang, source_lang=source_lang
    )
    return {
        "original_queries": queries,
        "translated_queries": translated_queries,
        "documents": documents,
        "target_language": target_lang,
        "source_language": source_lang,
    }
