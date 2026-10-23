from model_client import get_client, get_model
from model_models import text_from_payload, extract_message_content


def answer_with_context(payload, config=None):
    config = config or {}
    client = get_client(config)
    prompt = 'Answer the question using the provided context.\n\nContext:\n' + text_from_payload(payload, 'context') + '\n\nQuestion:\n' + text_from_payload(payload, 'question')
    response = client.chat.completions.create(model=get_model(config), messages=[{'role': 'user', 'content': prompt}])
    return {'answer': extract_message_content(response)}
