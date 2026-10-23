import os

from openai import OpenAI


def compliance_note_translate(note: str, target_language: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Translate to {target_language}."},
            {"role": "user", "content": note},
        ],
    )
    return response.choices[0].message.content
