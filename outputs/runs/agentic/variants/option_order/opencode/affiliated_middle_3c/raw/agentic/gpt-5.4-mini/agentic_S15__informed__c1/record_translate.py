from openai import OpenAI


def record_translate(text: str, target_language: str) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": f"Translate the user's text to {target_language}.",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content or ""
