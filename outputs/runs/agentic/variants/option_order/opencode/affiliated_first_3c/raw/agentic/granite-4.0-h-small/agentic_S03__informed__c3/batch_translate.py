from translation_client import normalize_request, normalize_response
from translation_models import TranslationRequest, TranslationResponse
from translation_client import get_translation_service_client


def batch_translate(
    texts: list[str], source_lang: str, target_lang: str, provider: str = "deepl"
) -> list[TranslationResponse]:
    """
    Translate a list of strings while preserving order.
    Under the hood each string is sent to the provider individually; some SDKs expose
    batch endpoints – adapt the call to those when available.

    Args:
        texts: list of source strings.
        source_lang: ISO 639‑1 source language.
        target_lang: ISO 639‑1 target language.
        provider: Translation provider identifier.

    Returns:
        List of TranslationResponse objects in the same order as `texts`.
    """
    client = get_translation_service_client(provider)
    results = []
    for text in texts:
        payload = {
            "text": text,
            "source": source_lang,
            "target": target_lang,
        }
        response = client.translate_text(
            **normalize_request(TranslationRequest(**payload), provider)
        )
        results.append(normalize_response(response, provider))
    return results
