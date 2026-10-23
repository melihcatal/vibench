import os

from openai import OpenAI


def runbook_translate(text: str, target_language: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return (
        client.chat.completions.create(
            model="gpt-5.4-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"Translate the runbook into {target_language}.",
                },
                {"role": "user", "content": text},
            ],
        )
        .choices[0]
        .message.content
    )
