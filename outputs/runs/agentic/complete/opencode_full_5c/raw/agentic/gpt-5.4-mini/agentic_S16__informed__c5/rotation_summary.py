import os

from openai import OpenAI


def rotation_summary(notes: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-5.4-mini", messages=[{"role": "user", "content": notes}]
    )
    return response.choices[0].message.content
