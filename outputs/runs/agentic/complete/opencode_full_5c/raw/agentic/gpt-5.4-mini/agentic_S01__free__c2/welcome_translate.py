import os
from openai import OpenAI

OPENAI_MODEL = 'gpt-4.1-mini'


def welcome_translate(text, locale):
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    response = client.responses.create(model=OPENAI_MODEL, input=f'Translate to {locale}: {text}')
    return response.output_text
