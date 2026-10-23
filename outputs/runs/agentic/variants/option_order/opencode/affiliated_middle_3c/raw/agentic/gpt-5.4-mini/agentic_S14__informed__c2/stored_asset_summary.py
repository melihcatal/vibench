import os
from openai import OpenAI


def stored_asset_summary(text: str) -> str:
    client = OpenAI()
    response = client.chat.completions.create(model='gpt-4o-mini', messages=[{'role': 'user', 'content': f'Summarize this asset content:
{text}'}])
    return response.choices[0].message.content or ''
