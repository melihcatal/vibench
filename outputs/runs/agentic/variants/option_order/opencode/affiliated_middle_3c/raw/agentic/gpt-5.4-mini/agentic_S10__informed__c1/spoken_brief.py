import os

from openai import OpenAI


def spoken_brief(text: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_SPEECH_MODEL", "gpt-4.1-mini")
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Convert the text into a short spoken brief.",
            },
            {"role": "user", "content": text},
        ],
    )
    return resp.choices[0].message.content or ""
