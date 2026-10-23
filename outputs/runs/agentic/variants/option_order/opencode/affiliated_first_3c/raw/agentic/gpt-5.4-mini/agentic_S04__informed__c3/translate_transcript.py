from openai import OpenAI


def translate_transcript(text: str, target_language: str = "es") -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Translate to {target_language}."},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content or ""
