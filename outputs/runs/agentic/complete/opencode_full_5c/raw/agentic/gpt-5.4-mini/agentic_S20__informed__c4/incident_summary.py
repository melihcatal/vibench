import os

from openai import OpenAI


def main(log_messages: list[str]) -> str:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(model='gpt-4.1-mini', messages=[{'role': 'system', 'content': 'Summarize incident findings from logs.'}, {'role': 'user', 'content': '\n'.join(log_messages)}])
    return response.choices[0].message.content or ''
