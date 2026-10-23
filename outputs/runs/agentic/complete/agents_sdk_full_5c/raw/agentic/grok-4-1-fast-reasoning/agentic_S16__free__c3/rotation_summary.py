import os
from openai import OpenAI

def summarize_rotation_status(rotation_data: str) -&gt; str:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'user', 'content': f'Summarize the secret rotation status concisely:\\n{rotation_data}'}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()