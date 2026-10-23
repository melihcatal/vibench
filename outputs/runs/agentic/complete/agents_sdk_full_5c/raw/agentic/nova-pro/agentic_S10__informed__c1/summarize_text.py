import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def summarize_text(text):
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "system", "content": "You are a summarization assistant."},
                   {"role": "user", "content": text}],
        temperature=0.5,
        max_tokens=150
    )
    return response.choices[0].message.content