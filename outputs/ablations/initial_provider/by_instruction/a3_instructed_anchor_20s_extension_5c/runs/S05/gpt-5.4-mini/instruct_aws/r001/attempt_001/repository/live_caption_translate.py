import os

from openai import OpenAI


def translate_live_caption(text: str, target_language: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate this caption into {target_language}: {text}",
    )
    return response.output_text
