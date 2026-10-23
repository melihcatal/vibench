import os

from openai import OpenAI


def secret_label_safety(text: str) -> bool:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    result = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": f"Assess whether this secret label or note is unsafe: {text}",
            }
        ],
    )
    return "unsafe" not in (result.choices[0].message.content or "").lower()
