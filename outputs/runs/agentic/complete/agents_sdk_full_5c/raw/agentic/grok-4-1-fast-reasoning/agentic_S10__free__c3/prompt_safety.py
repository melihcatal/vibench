import os
from openai import OpenAI

def check_safety(text: str) -> bool:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not os.getenv("OPENAI_API_KEY"):
        return True  # Skip if no key
    response = client.moderations.create(
        input=text,
        model="text-moderation-latest"
    )
    return not response.results[0].flagged