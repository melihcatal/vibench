from openai import OpenAI


def compliance_note_translate(text: str, target_language: str) -> dict:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "Translate compliance notes clearly and conservatively.",
            },
            {"role": "user", "content": f"Translate to {target_language}: {text}"},
        ],
    )
    return {
        "provider": "OpenAI",
        "model": "gpt-4.1-mini",
        "translation": response.choices[0].message.content,
    }
