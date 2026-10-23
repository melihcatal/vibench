import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def summarize_onboarding(text):
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.completions.create(
        model="text-davinci-003",
        prompt=text,
        max_tokens=150,
    )
    return response.choices[0].text.strip()
