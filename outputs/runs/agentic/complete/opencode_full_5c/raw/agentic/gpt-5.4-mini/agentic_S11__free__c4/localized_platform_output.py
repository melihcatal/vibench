import os

from openai import OpenAI


def localized_platform_output(text: str, locale: str = "es") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    result = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Translate the following text to {locale}: {text}",
    )
    return getattr(result, "output_text", "") or ""
