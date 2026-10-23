import os

from openai import OpenAI

from identity_models import normalize_locale


def welcome_translate(text: str, locale: str):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    resp = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate into {normalize_locale(locale)}: {text}",
    )
    return resp.output_text
