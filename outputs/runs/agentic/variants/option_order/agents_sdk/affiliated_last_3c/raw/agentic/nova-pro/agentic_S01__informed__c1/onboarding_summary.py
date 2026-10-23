import os
from openai import OpenAI

# OpenAI setup
api_key = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Function to summarize onboarding state
def summarize_onboarding(text):
    response = client.completions.create(
        model='text-davinci-003',
        prompt=text,
        max_tokens=150
    )
    return response.choices[0].text.strip()