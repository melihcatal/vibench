from model_client import chat_completion
from model_models import get_context, get_question


def answer_with_context(payload, config=None):
    context = get_context(payload)
    question = get_question(payload)
    response = chat_completion([
        {'role': 'system', 'content': 'Answer using only the provided context when possible.'},
        {'role': 'user', 'content': 'Context:
    ], config=config)
    return {'answer': response.choices[0].message.content or ''}
