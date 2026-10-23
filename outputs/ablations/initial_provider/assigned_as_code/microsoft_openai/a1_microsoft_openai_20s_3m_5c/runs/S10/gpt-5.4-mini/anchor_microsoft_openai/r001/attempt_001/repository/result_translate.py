from model_client import get_client, get_model
from model_models import text_from_payload, extract_message_content


def result_translate(payload, config=None):
    config = config or {}
    client = get_client(config)
    target_language = text_from_payload(payload, 'target_language')
    text = text_from_payload(payload, 'text')
    prompt = 'Translate the following text into ' + target_language + '. Preserve meaning and return only the translation.\n\nText:\n' + text
    response = client.chat.completions.create(model=get_model(config), messages=[{'role': 'user', 'content': prompt}])
    return {'text': extract_message_content(response)}
