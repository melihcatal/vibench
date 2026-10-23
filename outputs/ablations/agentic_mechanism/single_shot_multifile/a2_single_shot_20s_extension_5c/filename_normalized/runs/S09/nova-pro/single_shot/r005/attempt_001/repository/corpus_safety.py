import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def check_corpus(text):
    response = client.moderations.create(input=text)
    return response.results[0].flagged