import os
from openai import OpenAI


def spoken_brief(text: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Rewrite the text as a short spoken brief."},
            {"role": "user", "content": text},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content or ""
