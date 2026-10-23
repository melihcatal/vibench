from openai import OpenAI

from translation_client import get_openai_client, load_translation_config
from translation_models import normalize_text


def unsafe_copy_check(text: str, locale: str) -> str:
    config = load_translation_config()
    client: OpenAI = get_openai_client()
    completion = client.responses.create(
        model=config.model,
        input=[
            {"role": "system", "content": "Check localized copy for unsafe or policy-violating content and return a brief verdict."},
            {"role": "user", "content": f"Locale: {normalize_text(locale)}
Text: {normalize_text(text)}"},
        ],
    )
    return completion.output_text.strip()
