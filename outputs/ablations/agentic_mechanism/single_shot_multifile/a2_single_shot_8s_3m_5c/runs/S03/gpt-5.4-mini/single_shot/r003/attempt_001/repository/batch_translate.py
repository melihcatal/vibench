import os
from openai import OpenAI
from translation_client import get_openai_client, get_translation_model
from translation_models import BatchTranslationRequest, BatchTranslationResponse, normalize_batch_translation_text

_PROVIDER_MODEL = get_translation_model(os.getenv("TRANSLATION_MODEL", "gpt-4o-mini"))


def batch_translate(texts, source_language: str, target_language: str):
    client: OpenAI = get_openai_client()
    request = BatchTranslationRequest(texts=list(texts), source_language=source_language, target_language=target_language)
    response = client.responses.create(model=_PROVIDER_MODEL, input=request.to_prompt())
    output_text = getattr(response, "output_text", None)
    if not output_text:
        output_text = response.output[0].content[0].text
    normalized = normalize_batch_translation_text(output_text)
    return normalized.translated_texts
