from openai import OpenAI

from speech_client import client


def check_script_safety(text: str) -> bool:
    c: OpenAI = client()
    response = c.responses.create(model="omni-moderation-latest", input=text)
    return "unsafe" not in response.output_text.lower()
