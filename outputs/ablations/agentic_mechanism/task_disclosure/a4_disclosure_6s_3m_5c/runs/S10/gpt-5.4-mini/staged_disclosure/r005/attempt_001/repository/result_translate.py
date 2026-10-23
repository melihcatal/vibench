import os
from typing import Optional

from openai import OpenAI


def translate_result(text: str, target_language: str = "en", source_language: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    messages = [
        {
            "role": "system",
            "content": "You are a precise translation engine. Return only the translated text.",
        },
        {
            "role": "user",
            "content": (
                f"Translate the following text to {target_language}."
                + (f" Source language: {source_language}." if source_language else "")
                + f"\n\n{text}"
            ),
        },
    ]
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content or ""


if __name__ == "__main__":
    import sys

    input_text = sys.stdin.read()
    print(translate_result(input_text.strip()))
