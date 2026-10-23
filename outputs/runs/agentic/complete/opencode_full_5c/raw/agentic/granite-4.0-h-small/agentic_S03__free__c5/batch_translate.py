import os
from translation_client import TranslationClient
from translation_models import GeneralTextRequest, GeneralTextResponse


def batch_translate(
    texts: list[str], source_lang: str = "en", target_lang: str = "es"
) -> list[str]:
    """Translate a list of strings while preserving order.

    Args:
        texts: List of strings to translate.
        source_lang: ISO language code for source (default "en").
        target_lang: ISO language code for target (default "es").

    Returns:
        List of translated strings in the same order as input.
    """
    # Build batch payload
    payload = [
        GeneralTextRequest(
            source_text=t, source_lang=source_lang, target_lang=target_lang
        )
        for t in texts
    ]
    client = TranslationClient(model_id="openai/gpt-4o-mini")
    raw_results = client.batch_translate(payload)
    # raw_results is expected to be a list of dicts matching GeneralTextResponse
    results = [GeneralTextResponse.from_dict(r).translated_text for r in raw_results]
    return results
