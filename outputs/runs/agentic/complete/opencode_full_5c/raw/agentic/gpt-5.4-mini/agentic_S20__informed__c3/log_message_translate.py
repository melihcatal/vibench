import os
from typing import List

from openai import OpenAI


def translate_messages(messages: List[str], target_locale: str) -> List[str]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    model = "gpt-5.4-mini"
    translated = []
    for message in messages:
        response = client.responses.create(
            model=model,
            input=f"Translate this support-visible log message to {target_locale}: {message}",
        )
        translated.append(response.output_text)
    return translated
