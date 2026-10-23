import os

from openai import OpenAI


def translate_payload(text: str, target_language: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Translate this text to {target_language}: {text}",
            }
        ],
    )
    return response.choices[0].message.content or ""
