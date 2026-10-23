import os

from openai import OpenAI


def runbook_translate(text: str, target_language: str = "es") -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    result = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": f"Translate this secret-rotation runbook to {target_language}: {text}",
            }
        ],
    )
    return result.choices[0].message.content or ""
