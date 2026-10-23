import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def check_message_safety(payload: str) -> bool:
    response = client.moderations.create(
        model="text-moderation-latest",
        input=payload
    )
    moderation_output = response.results[0]
    return not moderation_output.flagged