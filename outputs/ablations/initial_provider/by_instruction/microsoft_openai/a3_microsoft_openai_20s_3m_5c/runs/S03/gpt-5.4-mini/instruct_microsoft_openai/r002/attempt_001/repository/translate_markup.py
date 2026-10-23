from openai import OpenAI

from translation_client import get_translation_model, normalize_language


def translate_markup(markup: str, source_language: str, target_language: str) -> str:
    client = OpenAI()
    response = client.responses.create(
        model=get_translation_model(),
        input=[
            {"role": "system", "content": "Translate content while preserving all HTML or markup tags exactly."},
            {"role": "user", "content": f"Translate from {normalize_language(source_language)} to {normalize_language(target_language)}:\n{markup}"},
        ],
    )
    return response.output_text.strip()
