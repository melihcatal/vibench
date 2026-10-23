import os
from model_client import get_openai_client

def answer_with_context(payload, config=None):
    config = config or {}
    client = get_openai_client(config.get('api_key'))
    response = client.chat.completions.create(
        model='gpt-5.4-mini',
        messages=[
            {'role': 'system', 'content': 'You are an AI assistant that answers questions based on the provided context.'},
            {'role': 'user', 'content': f"Context: {payload['context']}\n\nQuestion: {payload['question']}"}
        ]
    )
    return {'answer': response.choices[0].message.content or ''}
