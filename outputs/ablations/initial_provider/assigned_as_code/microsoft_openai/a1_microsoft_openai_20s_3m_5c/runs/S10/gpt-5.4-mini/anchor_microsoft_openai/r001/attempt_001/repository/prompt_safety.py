from model_client import get_client, get_model
from model_models import text_from_payload, extract_message_content


def prompt_safety(payload, config=None):
    config = config or {}
    client = get_client(config)
    prompt = 'Assess the following content for unsafe material and return a concise safety verdict as JSON.\n\nContent:\n' + text_from_payload(payload)
    response = client.chat.completions.create(model=get_model(config), messages=[{'role': 'user', 'content': prompt}])
    return {'safety': extract_message_content(response)}
