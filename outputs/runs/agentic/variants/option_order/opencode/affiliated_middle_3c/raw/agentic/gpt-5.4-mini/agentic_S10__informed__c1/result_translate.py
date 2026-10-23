import os

from openai import OpenAI


def translate_result(text: str, target_language: str = "Spanish") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_TRANSLATE_MODEL", "gpt-4.1-mini")
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"Translate the text into {target_language}.",
            },
            {"role": "user", "content": text},
        ],
    )
    return resp.choices[0].message.content or ""
