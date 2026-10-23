import os

from openai import OpenAI


def translate_consent_copy(text: str, target_language: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[{"role": "user", "content": f"Translate to {target_language}: {text}"}],
    )
    return response.output_text
