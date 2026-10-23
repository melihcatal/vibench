from model_client import chat_completion
from model_models import get_input_text


def result_translate(payload, config=None):
    text = get_input_text(payload)
    target_language = payload.get('target_language', 'English')
    response = chat_completion([
        {'role': 'system', 'content': 'Translate the text into the target language.'},
        {'role': 'user', 'content': 'Target language: ' + target_language + '\n\nText:\n' + text},
    ], config=config)
    return {'translation': response.choices[0].message.content or ''}
