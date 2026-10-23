import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def answer_with_context(question, context):
    response = client.completions.create(
        model='text-davinci-003',
        prompt=f'Answer the following question using the provided context: {question}. Context: {context}',
        max_tokens=100
    )
    return response.choices[0].text.strip()