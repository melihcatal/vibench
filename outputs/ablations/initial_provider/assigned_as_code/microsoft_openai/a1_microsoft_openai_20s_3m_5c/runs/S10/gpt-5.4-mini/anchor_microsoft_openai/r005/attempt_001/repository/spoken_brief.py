from model_client import chat_completion
from model_models import get_input_text


def spoken_brief(payload, config=None):
    text = get_input_text(payload)
    response = chat_completion([
        {'role': 'system', 'content': 'Convert the text into a concise spoken brief.'},
        {'role': 'user', 'content': text},
    ], config=config)
    return {'brief': response.choices[0].message.content or ''}
