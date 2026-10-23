from openai import OpenAI


def record_translate(text: str, target_language: str) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "user", "content": f"Translate to {target_language}: {text}"}
        ],
    )
    return response.choices[0].message.content or ""
