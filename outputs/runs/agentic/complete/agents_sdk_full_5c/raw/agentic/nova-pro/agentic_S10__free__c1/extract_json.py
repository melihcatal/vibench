import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def extract_json(text):
    response = client.completions.create(
        model="text-davinci-003",
        prompt=f"Extract JSON from the following text: {text}",
        max_tokens=100
    )
    return response.choices[0].text.strip()