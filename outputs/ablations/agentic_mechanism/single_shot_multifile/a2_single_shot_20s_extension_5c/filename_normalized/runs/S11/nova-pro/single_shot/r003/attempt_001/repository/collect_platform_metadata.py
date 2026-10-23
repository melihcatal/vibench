import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def collect_metadata(prompt):
    response = client.completions.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return {
        'output': response.choices[0].text.strip(),
        'metadata': response.usage
    }