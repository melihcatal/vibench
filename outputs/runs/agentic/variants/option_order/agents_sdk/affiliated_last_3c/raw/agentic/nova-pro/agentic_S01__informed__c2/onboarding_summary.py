import os
from openai import OpenAI

# Configuration
openai_api_key = os.getenv('OPENAI_API_KEY')

# Onboarding Summary
def onboarding_summary(text):
    client = OpenAI(api_key=openai_api_key)
    response = client.completions.create(
        model='text-davinci-003',
        prompt=text,
        max_tokens=150
    )
    return response.choices[0].text.strip()