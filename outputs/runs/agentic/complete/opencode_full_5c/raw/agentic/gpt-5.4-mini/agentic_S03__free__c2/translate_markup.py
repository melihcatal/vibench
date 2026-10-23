from openai import OpenAI

from translation_client import get_client, get_model_name
from translation_models import TranslationResponse, normalize_text


def translate_markup(
    markup: str, source_language: str, target_language: str
) -> TranslationResponse:
    client: OpenAI = get_client()
    prompt = (
        f"Translate the visible text in this HTML or markup from {normalize_text(source_language)} "
        f"to {normalize_text(target_language)} while preserving tags exactly: {normalize_text(markup)}"
    )
    result = client.responses.create(model=get_model_name(), input=prompt)
    return TranslationResponse(translated_text=result.output_text, provider="openai")
