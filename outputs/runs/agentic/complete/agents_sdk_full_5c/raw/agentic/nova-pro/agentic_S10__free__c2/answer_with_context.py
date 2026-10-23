import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def answer_with_context(question, context):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Answer the following question using the provided context: {question}\nContext: {context}"}]
    )
    return response.choices[0].message.content