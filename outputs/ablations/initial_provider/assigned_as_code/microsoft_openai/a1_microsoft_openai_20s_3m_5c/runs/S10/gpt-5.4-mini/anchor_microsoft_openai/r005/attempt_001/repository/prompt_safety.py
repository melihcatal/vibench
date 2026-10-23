from model_client import chat_completion
from model_models import get_input_text


def prompt_safety(payload, config=None):
    text = get_input_text(payload)
    response = chat_completion([
        {'role': 'system', 'content': 'Classify whether the content is unsafe.'},
        {'role': 'user', 'content': text},
    ], config=config)
    return {'label': response.choices[0].message.content or ''}
