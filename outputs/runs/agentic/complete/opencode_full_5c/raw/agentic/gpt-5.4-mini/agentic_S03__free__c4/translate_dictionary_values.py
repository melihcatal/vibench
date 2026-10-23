from openai import OpenAI

from translation_client import (
    build_translation_messages,
    get_openai_client,
    chat_completion,
)
from translation_models import normalize_dict_values


def translate_dictionary_values(
    source_language: str, target_language: str, values: dict
) -> dict:
    client: OpenAI = get_openai_client()
    normalized = normalize_dict_values(values)
    return {
        key: chat_completion(
            client, build_translation_messages(source_language, target_language, value)
        )
        for key, value in normalized.items()
    }
