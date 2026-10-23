import os
from typing import Dict

from openai import OpenAI


MODEL = "gpt-4.1-mini"


def welcome_translate(text: str, locale: str) -> Dict[str, str]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model=MODEL,
        input=f"Translate the following onboarding copy into {locale}: {text}",
    )
    return {"locale": locale, "translation": response.output_text}
