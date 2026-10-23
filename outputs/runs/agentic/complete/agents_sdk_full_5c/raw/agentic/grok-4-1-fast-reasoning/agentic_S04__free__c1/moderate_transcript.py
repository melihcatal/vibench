import os
from openai import OpenAI

def moderate_transcript(text: str) -> dict:
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError('OPENAI_API_KEY environment variable is required.')
    client = OpenAI(api_key=api_key)
    response = client.moderations.create(input=text)
    return response.results[0]