import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def translate_output(output, target_language='es'):
    response = client.completions.create(
        model="text-davinci-003",
        prompt=f'Translate the following to {target_language}: {output}',
        max_tokens=150
    )
    return response.choices[0].text.strip()