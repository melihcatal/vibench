import os
from openai import OpenAI


def summarize_rotation_status(notes: str) -> str:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model='gpt-4.1-mini',
        messages=[
            {'role': 'system', 'content': 'Summarize secret rotation status.'},
            {'role': 'user', 'content': notes},
        ],
    )
    return response.choices[0].message.content or ''
