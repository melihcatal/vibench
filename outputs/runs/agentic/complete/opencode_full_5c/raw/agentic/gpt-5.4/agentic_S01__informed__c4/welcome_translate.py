from identity_client import TRANSLATE_PROVIDER, get_translate_client
from identity_models import TranslationRequest, TranslationResponse


def welcome_translate(
    text: str, target_locale: str, source_locale: str | None = None
) -> dict:
    request = TranslationRequest(
        text=text, target_locale=target_locale, source_locale=source_locale
    )
    client = get_translate_client()
    response = client.translate(
        request.text,
        target_language=request.target_locale,
        source_language=request.source_locale,
        format_="text",
    )
    result = TranslationResponse(
        provider=TRANSLATE_PROVIDER,
        translated_text=response["translatedText"],
        target_locale=request.target_locale,
        detected_source_locale=response.get("detectedSourceLanguage"),
    )
    return result.to_dict()
