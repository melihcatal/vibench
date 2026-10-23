import os
from typing import Iterable, List

from openai import OpenAI


OPENAI_MODEL = "openai/gpt-5.4-mini"


def translate_log_messages(messages: Iterable[str], target_locale: str) -> List[str]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    payload = "\n".join(f"- {message}" for message in messages)
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": (
                    "Translate support-visible log messages into the target locale. "
                    "Preserve placeholders, IDs, timestamps, paths, codes, and technical terms. "
                    "Return one translated message per input line, in the same order, with no extra text."
                ),
            },
            {
                "role": "user",
                "content": f"Target locale: {target_locale}\n\nMessages:\n{payload}",
            },
        ],
    )
    translated = response.output_text.splitlines()
    return [line.lstrip("- ").strip() for line in translated if line.strip()]
