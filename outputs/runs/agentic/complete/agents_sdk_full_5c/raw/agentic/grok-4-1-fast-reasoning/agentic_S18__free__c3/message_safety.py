import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def check_message_safety(payload_text: str) -> bool:
    response = client.moderations.create(
        input=payload_text
    )
    result = response.results[0]
    return not result.flagged