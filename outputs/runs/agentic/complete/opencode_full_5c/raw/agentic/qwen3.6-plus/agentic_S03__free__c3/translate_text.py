from translation_models import TranslationRequest, TranslationResult
from translation_client import get_openai_client, translate_single_text


def translate_text(
    text: str,
    source_language: str = "auto",
    target_language: str = "en",
    context: str = None,
    custom_instructions: str = None,
) -> TranslationResult:
    client = get_openai_client()
    request = TranslationRequest(
        text=text,
        source_language=source_language,
        target_language=target_language,
        preserve_formatting=False,
        context=context,
        custom_instructions=custom_instructions,
    )
    return translate_single_text(client, request)
