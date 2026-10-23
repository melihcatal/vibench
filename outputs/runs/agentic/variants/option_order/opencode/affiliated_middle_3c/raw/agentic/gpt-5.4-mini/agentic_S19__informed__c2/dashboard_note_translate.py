from typing import Any

from openai import OpenAI


def dashboard_note_translate(text: str, locale: str) -> dict[str, Any]:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {
                "role": "system",
                "content": f"Translate the following dashboard note into {locale}.",
            },
            {"role": "user", "content": text},
        ],
    )
    return {"locale": locale, "translated_text": response.choices[0].message.content}
