import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def answer_with_context(question, context):
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "system", "content": "You are a question answering bot."},
                   {"role": "user", "content": f'{context} Question: {question}'}]
    )
    return response.choices[0].message.content