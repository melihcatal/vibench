import openai
import os

def message_summary(text: str) -> str:
    """
    Summarize message processing results
    """
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    if not client.api_key:
        raise ValueError('OPENAI_API_KEY required')
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': f'Summarize: {text}'}],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()