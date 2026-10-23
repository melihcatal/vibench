import os
from openai import OpenAI

def check_script_safety_openai(text: str) -> dict:
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    client = OpenAI(api_key=api_key)
    response = client.moderations.create(input=text, model="text-moderation-latest")
    return response.model_dump()
