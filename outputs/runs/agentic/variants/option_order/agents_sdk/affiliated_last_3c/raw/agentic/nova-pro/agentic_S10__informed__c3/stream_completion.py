import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def stream_completion(prompt):
    response = client.completions.create(
        model='text-davinci-003',
        prompt=prompt,
        max_tokens=100,
        stream=True
    )
    for chunk in response:
        yield chunk.choices[0].text.strip()