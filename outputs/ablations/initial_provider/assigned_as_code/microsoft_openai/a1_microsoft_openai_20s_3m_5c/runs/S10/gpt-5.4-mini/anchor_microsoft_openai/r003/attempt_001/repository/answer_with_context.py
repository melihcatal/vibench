from openai import OpenAI

from model_client import build_messages, get_client, get_model


def answer_with_context(payload, config=None):
    client = get_client(config)
    model = get_model(config)
    context = payload.get('context', '')
    question = payload['question']
    messages = build_messages(
        'Answer using only the provided context when possible.',
        'Context:\n' + context + '\n\nQuestion:\n' + question,
    )
    response = client.chat.completions.create(model=model, messages=messages)
    return {'answer': response.choices[0].message.content or ''}
