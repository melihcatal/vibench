import os
from openai import OpenAI

def summarize_onboarding(text):
    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)
    response = client.Completion.create(
        engine='text-davinci-002',
        prompt=text,
        max_tokens=150
    )
    return response.choices[0].text.strip()