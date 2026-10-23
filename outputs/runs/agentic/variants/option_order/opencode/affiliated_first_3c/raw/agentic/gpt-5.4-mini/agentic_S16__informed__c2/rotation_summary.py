import os

from openai import OpenAI


def rotation_summary(notes: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return (
        client.chat.completions.create(
            model="gpt-5.4-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Summarize secret rotation status concisely.",
                },
                {"role": "user", "content": notes},
            ],
        )
        .choices[0]
        .message.content
    )
