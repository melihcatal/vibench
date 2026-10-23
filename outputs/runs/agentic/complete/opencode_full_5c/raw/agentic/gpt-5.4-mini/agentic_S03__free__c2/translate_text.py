from openai import OpenAI

from translation_client import get_client, get_model_name
from translation_models import TranslationRequest, TranslationResponse, normalize_text


def translate_text(
    source_text: str, source_language: str, target_language: str
) -> TranslationResponse:
    request = TranslationRequest(
        source_text=normalize_text(source_text),
        source_language=normalize_text(source_language),
        target_language=normalize_text(target_language),
    )
    client: OpenAI = get_client()
    prompt = f"Translate from {request.source_language} to {request.target_language}: {request.source_text}"
    result = client.responses.create(model=get_model_name(), input=prompt)
    return TranslationResponse(translated_text=result.output_text, provider="openai")
