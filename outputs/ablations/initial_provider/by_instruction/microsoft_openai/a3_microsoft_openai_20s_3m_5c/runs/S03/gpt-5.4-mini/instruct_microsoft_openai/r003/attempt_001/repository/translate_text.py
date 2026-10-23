from openai import OpenAI

from translation_client import get_openai_client, translation_model, translate_prompt
from translation_models import TranslationRequest, TranslationResult, normalize_text


def translate_text(request: TranslationRequest) -> TranslationResult:
    client: OpenAI = get_openai_client()
    response = client.responses.create(
        model=translation_model(),
        input=translate_prompt(request.source_language, request.target_language, normalize_text(request.text)),
    )
    translated_text = response.output_text.strip()
    return TranslationResult(translated_text=translated_text, source_language=request.source_language, target_language=request.target_language, provider="openai", raw=response.model_dump())
