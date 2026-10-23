from openai import OpenAI

from translation_client import get_openai_client, translation_model, translate_prompt
from translation_models import TranslationResult


def translate_dictionary_values(data: dict[str, str], source_language: str, target_language: str) -> dict[str, TranslationResult]:
    client: OpenAI = get_openai_client()
    output: dict[str, TranslationResult] = {}
    for key, value in data.items():
        response = client.responses.create(
            model=translation_model(),
            input=translate_prompt(source_language, target_language, value),
        )
        output[key] = TranslationResult(translated_text=response.output_text.strip(), source_language=source_language, target_language=target_language, provider="openai", raw=response.model_dump())
    return output
