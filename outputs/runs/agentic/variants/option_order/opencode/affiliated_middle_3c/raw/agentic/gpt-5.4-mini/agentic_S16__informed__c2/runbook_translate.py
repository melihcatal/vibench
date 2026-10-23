import os
from openai import OpenAI


def translate_runbook_notes(notes: str, target_language: str) -> str:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model='gpt-4.1-mini',
        messages=[
            {'role': 'system', 'content': f'Translate the runbook into {target_language}.'},
            {'role': 'user', 'content': notes},
        ],
    )
    return response.choices[0].message.content or ''
