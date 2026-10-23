from openai import OpenAI

from translation_client import get_openai_client, load_translation_config
from translation_models import DictionaryTranslationResponse, normalize_mapping_values


def translate_dictionary_values(data, source_language: str, target_language: str) -> DictionaryTranslationResponse:
    config = load_translation_config()
    client: OpenAI = get_openai_client()
    normalized = normalize_mapping_values(data)
    completion = client.responses.create(
        model=config.model,
        input=[
            {"role": "system", "content": "Translate only mapping values while preserving keys and JSON object shape."},
            {"role": "user", "content": f"Translate from {source_language} to {target_language} the following JSON object values and return JSON only:
{normalized}"},
        ],
    )
    return DictionaryTranslationResponse(translated_values={k: v for k, v in normalized.items()}, provider="openai")
