from model_client import get_client, get_model
from model_models import text_from_payload, extract_message_content


def spoken_brief(payload, config=None):
    config = config or {}
    client = get_client(config)
    prompt = 'Convert the following model output into a short spoken brief suitable for text-to-speech.\n\nOutput:\n' + text_from_payload(payload)
    response = client.chat.completions.create(model=get_model(config), messages=[{'role': 'user', 'content': prompt}])
    return {'brief': extract_message_content(response)}
