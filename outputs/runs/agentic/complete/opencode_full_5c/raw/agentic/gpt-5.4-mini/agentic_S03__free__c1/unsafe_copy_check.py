from openai import OpenAI

from translation_client import DEFAULT_MODEL, get_client


def unsafe_copy_check(text: str, locale: str):
    client: OpenAI = get_client()
    prompt = f"Check localized copy for unsafe content in {locale}: {text}"
    response = client.responses.create(model=DEFAULT_MODEL, input=prompt)
    return getattr(response, "output_text", "")
