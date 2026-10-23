import os

from openai import OpenAI


def compliance_note_translate(text: str, target_language: str = "en") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"Translate compliance notes to {target_language}.",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content or ""
