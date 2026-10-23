import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def is_message_safe(text: str) -> bool:
    if not text or not text.strip():
        return True
    response = client.moderations.create(input=text)
    return not response.results[0].flagged
