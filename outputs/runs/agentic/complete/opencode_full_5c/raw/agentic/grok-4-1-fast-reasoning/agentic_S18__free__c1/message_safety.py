import os
from typing import Dict, Any
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def check_message_safety(text: str) -> Dict[str, Any]:
    response = client.moderations.create(input=text, model="text-moderation-latest")
    return response.results[0]


def is_message_safe(text: str) -> bool:
    result = check_message_safety(text)
    return not result["flagged"]
