from openai import OpenAI

from model_models import normalize_text


def localized_platform_output(text: str, locale: str) -> str:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate the following into {locale}: {normalize_text(text)}",
    )
    return normalize_text(getattr(response, "output_text", None))
