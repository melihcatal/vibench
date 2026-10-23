from openai import OpenAI

from translation_client import get_openai_client, translation_model, translate_prompt
from translation_models import BatchTranslationRequest, TranslationResult, normalize_texts


def batch_translate(request: BatchTranslationRequest) -> list[TranslationResult]:
    client: OpenAI = get_openai_client()
    results: list[TranslationResult] = []
    for text in normalize_texts(request.texts):
        response = client.responses.create(
            model=translation_model(),
            input=translate_prompt(request.source_language, request.target_language, text),
        )
        results.append(TranslationResult(translated_text=response.output_text.strip(), source_language=request.source_language, target_language=request.target_language, provider="openai", raw=response.model_dump()))
    return results
