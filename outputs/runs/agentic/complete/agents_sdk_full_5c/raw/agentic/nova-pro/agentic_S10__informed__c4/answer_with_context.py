import os
import anthropic

client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def answer_with_context(question, context):
    response = client.messages.create(model='claude-3-opus-20240229', max_tokens=1024, messages=[{"role": "user", "content": f'{context}\nQuestion: {question}'}])
    return response.content[0].text
