import os
from openai import OpenAI

def check_platform_output_safety(text: str) -> bool:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(input=text)
    return not response.results[0].flagged
