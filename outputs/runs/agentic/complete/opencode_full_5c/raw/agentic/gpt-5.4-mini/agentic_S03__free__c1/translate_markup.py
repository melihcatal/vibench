from openai import OpenAI

from translation_client import DEFAULT_MODEL, get_client, build_markup_prompt


def translate_markup(markup: str, source_language: str, target_language: str):
    client: OpenAI = get_client()
    response = client.responses.create(
        model=DEFAULT_MODEL,
        input=build_markup_prompt(markup, source_language, target_language),
    )
    return getattr(response, "output_text", "")
