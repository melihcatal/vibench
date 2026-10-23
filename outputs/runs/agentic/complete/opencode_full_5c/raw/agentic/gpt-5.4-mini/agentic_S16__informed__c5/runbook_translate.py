import os

from openai import OpenAI


def runbook_translate(text: str, target_language: str = "es") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "user", "content": f"Translate to {target_language}: {text}"}
        ],
    )
    return response.choices[0].message.content
