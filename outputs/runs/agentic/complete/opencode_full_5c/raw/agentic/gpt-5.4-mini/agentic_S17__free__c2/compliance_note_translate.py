import os
from openai import OpenAI

def compliance_note_translate(text: str, target_language: str = 'en') -> str:
    client = OpenAI()
    response = client.responses.create(model='gpt-5.4-mini', input=f'Translate compliance note to {target_language}: {text}')
    return response.output_text

if __name__ == '__main__':
    print(compliance_note_translate(os.getenv('NOTE', '')))
