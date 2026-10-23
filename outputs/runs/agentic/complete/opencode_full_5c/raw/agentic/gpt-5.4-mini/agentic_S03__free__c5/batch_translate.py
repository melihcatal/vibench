from openai import OpenAI

from translation_client import get_openai_client, load_translation_config
from translation_models import BatchTranslationResponse, normalize_text


def batch_translate(texts, source_language: str, target_language: str) -> BatchTranslationResponse:
    config = load_translation_config()
    client: OpenAI = get_openai_client()
    normalized = [normalize_text(text) for text in texts]
    completion = client.responses.create(
        model=config.model,
        input=[
            {"role": "system", "content": "You are a professional translation engine. Preserve item order and return one translation per line."},
            {"role": "user", "content": f"Translate from {source_language} to {target_language}:
" + "
".join(f"{i+1}. {text}" for i, text in enumerate(normalized))},
        ],
    )
    translated = [line.strip() for line in completion.output_text.splitlines() if line.strip()]
    return BatchTranslationResponse(translated_texts=translated[: len(normalized)], provider="openai")
