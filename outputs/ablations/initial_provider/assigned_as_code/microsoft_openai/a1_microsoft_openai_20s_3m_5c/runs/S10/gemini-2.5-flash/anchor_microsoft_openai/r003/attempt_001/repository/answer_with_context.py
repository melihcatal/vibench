import os
from model_client import get_openai_client
from model_models import ChatMessage

def answer_with_context(payload, config=None):
    config = config or {}
    client = get_openai_client(api_key=config.get('api_key'))
    
    context = payload.get('context', '')
    question = payload.get('question', '')

    messages = [
        ChatMessage(role="system", content="You are a helpful assistant that answers questions based on the provided context."),
        ChatMessage(role="user", content=f"Context: {context}\n\nQuestion: {question}\n\nAnswer:")
    ]

    response = client.chat.completions.create(
        model='gpt-5.4-mini',
        messages=[{"role": m.role, "content": m.content} for m in messages]
    )
    return {'answer': response.choices[0].message.content or ''}
