from openai import OpenAI

from translation_client import get_openai_client, load_translation_config
from translation_models import MarkupTranslationResponse, normalize_text


def translate_markup(markup: str, source_language: str, target_language: str) -> MarkupTranslationResponse:
    config = load_translation_config()
    client: OpenAI = get_openai_client()
    completion = client.responses.create(
        model=config.model,
        input=[
            {"role": "system", "content": "You translate HTML or markup while preserving all tags, attributes, and structure. Return only the translated markup."},
            {"role": "user", "content": f"Translate from {normalize_text(source_language)} to {normalize_text(target_language)}:
{normalize_text(markup)}"},
        ],
    )
    return MarkupTranslationResponse(translated_markup=completion.output_text.strip(), provider="openai")
