import os

from openai import OpenAI


def compliance_note_translate(text: str, target_language: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Translate compliance and encryption notes."},
            {"role": "user", "content": f"Translate to {target_language}: {text}"},
        ],
    )
    return response.choices[0].message.content
