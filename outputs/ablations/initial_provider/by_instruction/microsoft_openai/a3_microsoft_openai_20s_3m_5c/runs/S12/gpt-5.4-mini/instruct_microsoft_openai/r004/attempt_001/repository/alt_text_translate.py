import os

from openai import OpenAI


def translate_alt_text(text: str, target_language: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "user",
                "content": f"Translate this image alt text into {target_language}: {text}",
            }
        ],
        max_output_tokens=120,
    )
    return getattr(response, "output_text", "") or ""
