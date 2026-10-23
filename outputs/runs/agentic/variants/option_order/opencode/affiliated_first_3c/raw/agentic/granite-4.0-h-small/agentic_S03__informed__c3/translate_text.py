from translation_client import (
    get_translation_service_client,
    normalize_request,
    normalize_response,
)
from translation_models import TranslationRequest, TranslationResponse


def translate_text(
    source_lang: str, target_lang: str, text: str, provider: str = "deepl"
) -> TranslationResponse:
    """
    Translate a single string between two language codes (ISO 639‑1) using the chosen provider.

    Args:
        source_lang: Source language code (e.g., "en").
        target_lang: Target language code (e.g., "fr").
        text: The text to translate.
        provider: Provider identifier (deepl|google|amazon|azure|alibaba|watsonx).

    Returns:
        TranslationResponse with translated text and language metadata.
    """
    payload = {
        "text": text,
        "source": source_lang,
        "target": target_lang,
    }
    client = get_translation_service_client(provider)
    request = TranslationRequest(source=source_lang, target=target_lang, text=text)
    # send request to provider (simplified; each SDK may differ)
    # this example demonstrates a synchronous call; handle exceptions in real code.
    if provider == "deepl":
        # DeepL Python SDK wrapper (deepl package)
        response = client.translate_text(**normalize_request(request, provider))
    else:
        # most SDKs follow a similar pattern; adjust per provider as needed.
        response = getattr(client, "translate_text")(
            **normalize_request(request, provider)
        )
    return normalize_response(response, provider)
