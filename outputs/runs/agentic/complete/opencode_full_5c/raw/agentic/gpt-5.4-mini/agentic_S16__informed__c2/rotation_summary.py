import os

from openai import OpenAI


def rotation_summary(text: str) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    result = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": f"Summarize secret rotation status: {text}"}
        ],
    )
    return result.choices[0].message.content or ""
