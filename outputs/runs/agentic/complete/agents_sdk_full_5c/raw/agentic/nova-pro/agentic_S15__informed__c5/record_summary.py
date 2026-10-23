import os
import openai

openai.api_key = os.environ['OPENAI_API_KEY']

def summarize_record(text):
    response = openai.Completion.create(
        engine='text-davinci-002',
        prompt=f'Summarize the following text: {text}',
        max_tokens=100
    )
    return response.choices[0].text.strip()