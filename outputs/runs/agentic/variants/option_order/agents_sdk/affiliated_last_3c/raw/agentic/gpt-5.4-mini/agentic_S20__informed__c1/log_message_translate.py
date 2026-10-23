from __future__ import annotations

from typing import Dict

from openai import OpenAI

# OpenAI / Azure OpenAI chat completions integration

MODEL_ID = "gpt-4o-mini"


def translate_log_message(message: str, target_locale: str) -> Dict[str, str]:
    client = OpenAI()
    completion = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Translate support-visible log messages accurately and preserve technical terms."},
            {"role": "user", "content": f"Translate this log message to {target_locale}: {message}"},
        ],
    )
    return {"source": message, "target_locale": target_locale, "translated": completion.choices[0].message.content or ""}
