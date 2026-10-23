import os
from openai import OpenAI


def unsafe_copy_check(text: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {
                "role": "system",
                "content": "Assess localized copy for unsafe content and return a brief verdict.",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content or ""
