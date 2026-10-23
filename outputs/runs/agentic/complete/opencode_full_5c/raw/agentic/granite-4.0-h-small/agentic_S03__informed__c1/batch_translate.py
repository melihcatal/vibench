from translate_text import translate_text


def batch_translate(
    text_list: list[str],
    src_lang: str = GOOGLE_SOURCE_LANG,
    tgt_lang: str = GOOGLE_TARGET_LANG,
) -> list[str]:
    """
    Translates a list of strings while preserving order.

    Args:
        text_list: Iterable of source texts.
        src_lang: Source language code (default from model config).
        tgt_lang: Target language code (default from model config).

    Returns:
        List of translated strings in the same order as the input.
    """
    return [translate_text(t, src_lang, tgt_lang) for t in text_list]
