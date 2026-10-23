import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def check_safety(output):
    response = client.moderations.create(input=output)
    return response.results[0].flagged