import os
from openai import OpenAI

def moderate_profile_text(text: str) -> dict:
    api_key = os.environ["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
    response = client.moderations.create(input=text)
    return {
        "flagged": response.results[0]["flagged"],
        "categories": response.results[0]["categories"]
    }