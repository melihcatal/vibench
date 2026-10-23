import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def translate_appeal(text, target_language='es'):
    response = openai.Completion.create(engine='text-davinci-003', prompt=f'Translate the following to {target_language}: {text}', max_tokens=150)
    return response.choices[0].text.strip()