from translation_client import get_client, get_config
from translation_models import TranslationResponse, normalize_text


def translate_markup(markup: str, source_lang: str, target_lang: str) -> TranslationResponse:
    client = get_client()
    config = get_config()
    result = client.translate_text(
        normalize_text(markup),
        source_lang=source_lang,
        target_lang=target_lang,
        tag_handling='html',
        preserve_formatting=config.preserve_formatting,
        formality=config.formality,
    )
    return TranslationResponse(text=result.text, detected_source_lang=getattr(result, 'detected_source_lang', None))
