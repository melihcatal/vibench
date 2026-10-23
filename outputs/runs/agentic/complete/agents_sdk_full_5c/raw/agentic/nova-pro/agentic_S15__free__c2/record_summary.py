import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def summarize_record(text):
    response = openai.Completion.create(
        engine='text-davinci-002',
        prompt=f'Summarize the following text: {text}',
        max_tokens=60
    )
    return response.choices[0].text.strip()