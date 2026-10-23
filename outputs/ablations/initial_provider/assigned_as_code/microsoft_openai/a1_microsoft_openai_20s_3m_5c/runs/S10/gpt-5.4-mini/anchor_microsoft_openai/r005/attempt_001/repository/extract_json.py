from model_client import chat_completion
from model_models import get_input_text, get_json_schema


def extract_json(payload, config=None):
    text = get_input_text(payload)
    schema = get_json_schema(payload)
    response = chat_completion([
        {'role': 'system', 'content': 'Extract structured JSON from the user text.'},
        {'role': 'user', 'content': 'Return only JSON.
    ], config=config, response_format={'type': 'json_object'})
    return {'json': response.choices[0].message.content or ''}
