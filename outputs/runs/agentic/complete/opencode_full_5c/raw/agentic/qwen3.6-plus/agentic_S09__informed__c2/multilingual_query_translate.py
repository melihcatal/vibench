import os
import deepl


def translate_queries(queries, target_lang="EN"):
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    translated = []
    for query in queries:
        result = translator.translate_text(query, target_lang=target_lang)
        translated.append(result.text)

    return translated


def translate_and_prepare_for_search(queries, documents, target_lang="EN"):
    translated_queries = translate_queries(queries, target_lang=target_lang)

    translated_docs = []
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    for doc in documents:
        result = translator.translate_text(doc, target_lang=target_lang)
        translated_docs.append(result.text)

    return {
        "original_queries": queries,
        "translated_queries": translated_queries,
        "original_documents": documents,
        "translated_documents": translated_docs,
    }
