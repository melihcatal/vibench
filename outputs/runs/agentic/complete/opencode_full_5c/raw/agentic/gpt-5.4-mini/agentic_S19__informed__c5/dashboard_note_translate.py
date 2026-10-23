from typing import Dict

from openai import OpenAI


def dashboard_note_translate(text: str, locale: str) -> Dict[str, str]:
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": f"Translate the note to {locale}."},
            {"role": "user", "content": text},
        ],
    )
    return {"locale": locale, "translation": completion.choices[0].message.content}
