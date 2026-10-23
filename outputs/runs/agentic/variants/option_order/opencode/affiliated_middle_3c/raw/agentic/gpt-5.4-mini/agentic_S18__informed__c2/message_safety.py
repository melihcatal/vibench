import os

from openai import OpenAI


def check_message_safety(payload_text: str) -> bool:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.moderations.create(
        model="omni-moderation-latest", input=payload_text
    )
    return not response.results[0].flagged
