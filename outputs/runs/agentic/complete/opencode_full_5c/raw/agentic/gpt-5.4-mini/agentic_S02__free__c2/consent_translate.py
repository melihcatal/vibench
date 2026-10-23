import os

import openai


def translate_consent(text: str, target_language: str) -> str:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini", input=f"Translate to {target_language}: {text}"
    )
    return response.output_text
