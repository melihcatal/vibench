import os

from openai import OpenAI

from identity_client import load_config
from identity_models import normalize_locale


def welcome_translate(text: str, locale: str | None = None) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    target_locale = normalize_locale(locale or load_config().default_locale)
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": "Translate onboarding copy accurately and naturally."},
            {"role": "user", "content": f"Locale: {target_locale}\nText: {text}"},
        ],
    )
    return response.choices[0].message.content or ""
