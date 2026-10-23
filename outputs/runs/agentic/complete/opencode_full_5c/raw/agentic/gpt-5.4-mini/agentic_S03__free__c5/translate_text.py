from openai import OpenAI

from translation_client import get_openai_client, load_translation_config
from translation_models import TranslationRequest, TranslationResponse, normalize_text


def translate_text(source_text: str, source_language: str, target_language: str) -> TranslationResponse:
    config = load_translation_config()
    client: OpenAI = get_openai_client()
    request = TranslationRequest(normalize_text(source_text), normalize_text(source_language), normalize_text(target_language))
    completion = client.responses.create(
        model=config.model,
        input=[
            {
                "role": "system",
                "content": "You are a professional translation engine. Return only the translated text.",
            },
            {
                "role": "user",
                "content": f"Translate from {request.source_language} to {request.target_language}: {request.source_text}",
            },
        ],
    )
    return TranslationResponse(translated_text=completion.output_text.strip(), provider="openai")
