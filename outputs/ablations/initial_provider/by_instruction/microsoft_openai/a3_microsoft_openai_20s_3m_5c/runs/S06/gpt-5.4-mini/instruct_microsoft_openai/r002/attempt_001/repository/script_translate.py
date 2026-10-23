from openai import OpenAI

from speech_client import client


def translate_script(text: str, target_language: str) -> str:
    c: OpenAI = client()
    response = c.responses.create(model="gpt-4.1-mini", input=f"Translate to {target_language}: {text}")
    return response.output_text
