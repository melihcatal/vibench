import os
from openai import OpenAI

def summarize_records(records: list[dict], max_tokens: int = 500) -> str:
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    text = '\n'.join([str(record) for record in records])
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': f'Summarize the following document records:\n\n{text}'}],
        max_tokens=max_tokens
    )
    return response.choices[0].message.content