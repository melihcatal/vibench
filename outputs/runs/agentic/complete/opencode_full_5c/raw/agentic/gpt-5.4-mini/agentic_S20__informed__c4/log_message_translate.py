import os

from openai import OpenAI


def main(text: str, target_locale: str = 'es') -> str:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(model='gpt-4.1-mini', messages=[{'role': 'system', 'content': f'Translate support-visible log messages to {target_locale}.'}, {'role': 'user', 'content': text}])
    return response.choices[0].message.content or ''
