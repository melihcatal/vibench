import os
from openai import OpenAI

def is_message_safe(payload: str) -> bool:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(input=payload)
    return not response.results[0].flagged
