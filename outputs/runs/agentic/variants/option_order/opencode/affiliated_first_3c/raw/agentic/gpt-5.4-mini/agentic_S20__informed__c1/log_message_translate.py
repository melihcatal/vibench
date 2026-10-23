import os
from typing import Any, Dict

from openai import OpenAI


def log_message_translate(text: str, target_locale: str) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {
                "role": "system",
                "content": f"Translate the log message into {target_locale} while preserving meaning.",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content or ""


if __name__ == "__main__":
    log_message_translate("", "en-US")
