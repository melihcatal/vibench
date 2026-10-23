from openai import OpenAI

from translation_client import get_client, get_model_name
from translation_models import (
    TranslationResponse,
    normalize_mapping_values,
    normalize_text,
)


def translate_dictionary_values(
    values: dict[str, str], source_language: str, target_language: str
) -> dict[str, TranslationResponse]:
    client: OpenAI = get_client()
    model = get_model_name()
    normalized = normalize_mapping_values(values)
    output: dict[str, TranslationResponse] = {}
    for key, value in normalized.items():
        prompt = f"Translate from {normalize_text(source_language)} to {normalize_text(target_language)}: {value}"
        result = client.responses.create(model=model, input=prompt)
        output[key] = TranslationResponse(
            translated_text=result.output_text, provider="openai"
        )
    return output
