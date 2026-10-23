import os

from openai import OpenAI


def welcome_translate(text: str, locale: str) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Translate onboarding copy into the requested locale while preserving meaning.",
            },
            {"role": "user", "content": f"Locale: {locale}\nText: {text}"},
        ],
    )
    return response.output_text
