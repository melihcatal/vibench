import os
from translation_client import get_translation_client


def batch_translate(
    texts: list[str], source_lang: str = "en", target_lang: str = "es"
) -> list[str]:
    """Translate a list of strings while preserving order.

    Uses Amazon Translate as the concrete provider.
    """
    client = get_translation_client()
    responses = client.batch_translate_text(
        Texts=texts,
        SourceLanguageCode=source_lang,
        TargetLanguageCode=target_lang,
    )
    return [r.get("TranslatedText") for r in responses]
