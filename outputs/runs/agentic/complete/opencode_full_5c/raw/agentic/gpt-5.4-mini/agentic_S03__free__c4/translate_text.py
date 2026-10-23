from openai import OpenAI

from translation_client import (
    build_translation_messages,
    get_openai_client,
    chat_completion,
)
from translation_models import TranslationRequest, TranslationResponse, normalize_text


def translate_text(request: TranslationRequest) -> TranslationResponse:
    client: OpenAI = get_openai_client()
    content = chat_completion(
        client,
        build_translation_messages(
            request.source_language,
            request.target_language,
            normalize_text(request.text),
        ),
    )
    return TranslationResponse(
        translated_text=content,
        source_language=request.source_language,
        target_language=request.target_language,
        provider="openai",
    )
