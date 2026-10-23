from openai import OpenAI

from translation_client import get_openai_client, load_translation_config
from translation_models import normalize_text


def quality_summary(source_text: str, translated_text: str, source_language: str, target_language: str) -> str:
    config = load_translation_config()
    client: OpenAI = get_openai_client()
    completion = client.responses.create(
        model=config.model,
        input=[
            {"role": "system", "content": "Summarize translation quality issues concisely for editorial review."},
            {"role": "user", "content": f"Source ({source_language}): {normalize_text(source_text)}
Translation ({target_language}): {normalize_text(translated_text)}"},
        ],
    )
    return completion.output_text.strip()
