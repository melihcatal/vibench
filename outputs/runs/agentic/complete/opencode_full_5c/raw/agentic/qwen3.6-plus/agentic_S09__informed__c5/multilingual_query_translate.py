import os
import deepl


def translate_queries(queries, target_lang="EN", auth_key=None):
    auth_key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    translator = deepl.Translator(auth_key)
    if isinstance(queries, str):
        queries = [queries]
    texts_to_translate = [q for q in queries if not q.isascii() or len(q.strip()) > 0]
    if not texts_to_translate:
        return {q: q for q in queries}
    result = translator.translate_text(
        texts_to_translate,
        target_lang=target_lang,
    )
    translations = []
    if isinstance(result, list):
        translations = [r.text for r in result]
    else:
        translations = [result.text]
    translated_map = {}
    idx = 0
    for q in queries:
        if q in texts_to_translate:
            translated_map[q] = translations[idx]
            idx += 1
        else:
            translated_map[q] = q
    return translated_map
