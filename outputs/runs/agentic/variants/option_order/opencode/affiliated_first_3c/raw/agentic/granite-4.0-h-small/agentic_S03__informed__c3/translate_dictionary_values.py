from translation_client import normalize_request, normalize_response
from translation_models import TranslationRequest, TranslationResponse
from translation_client import get_translation_service_client


def translate_dict_values(
    input_dict: dict, source_lang: str, target_lang: str, provider: str = "deepl"
) -> dict:
    """
    Translate every **string** value in a dictionary while keeping the keys unchanged.
    Nested dictionaries are **not** traversed – only top‑level values are translated.

    Args:
        input_dict: dict with string values to translate.
        source_lang: ISO 639‑1 source language (e.g., "en").
        target_lang: ISO 639‑1 target language (e.g., "es").
        provider: Translation provider identifier.

    Returns:
        A new dictionary with the same keys and translated string values.
    """
    output = {}
    client = get_translation_service_client(provider)
    for key, raw_value in input_dict.items():
        if isinstance(raw_value, str):
            payload = {
                "text": raw_value,
                "source": source_lang,
                "target": target_lang,
            }
            response = client.translate_text(
                **normalize_request(TranslationRequest(**payload), provider)
            )
            output[key] = normalize_response(response, provider)["translated_text"]
        else:
            # non‑string values are left untouched
            output[key] = raw_value
    return output
