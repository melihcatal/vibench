from openai import OpenAI


def summarize_incident(error_logs: list[str]) -> str:
    client = OpenAI()
    response = client.chat.completions.create(model='gpt-4o-mini', messages=[{'role': 'user', 'content': '
'.join(error_logs)}])
    return response.choices[0].message.content or ''
