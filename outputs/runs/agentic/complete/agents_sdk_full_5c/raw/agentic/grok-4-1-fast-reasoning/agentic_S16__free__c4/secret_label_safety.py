import os

def check_secret_label_safety(label: str, notes: str = '') -> bool:
    text = f'{label} {notes}'.strip()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError('OPENAI_API_KEY environment variable required')
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    response = client.moderations.create(input=text)
    return not response.results[0].flagged