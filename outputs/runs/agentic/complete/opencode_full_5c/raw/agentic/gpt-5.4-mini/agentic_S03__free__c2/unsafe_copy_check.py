from openai import OpenAI

from translation_client import get_client, get_model_name
from translation_models import normalize_text


def unsafe_copy_check(text: str, locale: str) -> str:
    client: OpenAI = get_client()
    prompt = (
        f"Check this localized copy for unsafe, misleading, or policy-violating content in {normalize_text(locale)}: "
        f"{normalize_text(text)}"
    )
    result = client.responses.create(model=get_model_name(), input=prompt)
    return result.output_text
