import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def check_unsafe_content(text: str) -> bool:
    """Returns True if content is unsafe."""
    response = client.moderations.create(
        model="text-moderation-latest",
        input=text
    )
    return response.results[0].flagged