import os
from typing import Iterable

from openai import OpenAI


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def translate_log_messages(messages: Iterable[str], locale: str) -> list[str]:
    items = list(messages)
    if not items:
        return []
    prompt = (
        "Translate the following support-visible log messages into the target locale. "
        "Preserve meaning, identifiers, placeholders, timestamps, codes, and product names. "
        "Return only a JSON array of translated strings in the same order. "
        f"Target locale: {locale}\n\n"
        + "\n".join(f"- {message}" for message in items)
    )
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt,
    )
    text = response.output_text.strip()
    if text.startswith("```"):
        text = text.strip("`")
    import json

    translated = json.loads(text)
    if not isinstance(translated, list) or len(translated) != len(items):
        raise ValueError("Unexpected translation response")
    return [str(entry) for entry in translated]


def translate_log_message(message: str, locale: str) -> str:
    return translate_log_messages([message], locale)[0]
