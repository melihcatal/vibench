from openai import OpenAI

from translation_client import (
    build_translation_messages,
    get_openai_client,
    chat_completion,
)
from translation_models import BatchTranslationRequest, normalize_text_list


def batch_translate(request: BatchTranslationRequest) -> list[str]:
    client: OpenAI = get_openai_client()
    results: list[str] = []
    for text in normalize_text_list(request.texts):
        results.append(
            chat_completion(
                client,
                build_translation_messages(
                    request.source_language, request.target_language, text
                ),
            )
        )
    return results
