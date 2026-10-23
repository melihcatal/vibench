import os
import deepl

DEEPL_TARGET_LANG = os.getenv("DEEPL_TARGET_LANG", "EN")


def translate_queries(
    queries: list[str],
    source_lang: str | None = None,
    target_lang: str | None = None,
    auth_key: str | None = None,
) -> list[str]:
    key = auth_key or os.getenv("DEEPL_AUTH_KEY")
    if not key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    target = target_lang or DEEPL_TARGET_LANG
    translator = deepl.Translator(key)
    if not queries:
        return []
    if source_lang:
        result = translator.translate_text(
            queries,
            source_lang=source_lang,
            target_lang=target,
        )
    else:
        result = translator.translate_text(
            queries,
            target_lang=target,
        )
    if isinstance(result, list):
        return [r.text for r in result]
    return [result.text]


def translate_query(
    query: str,
    source_lang: str | None = None,
    target_lang: str | None = None,
    auth_key: str | None = None,
) -> str:
    translated = translate_queries(
        [query],
        source_lang=source_lang,
        target_lang=target_lang,
        auth_key=auth_key,
    )
    return translated[0] if translated else query
