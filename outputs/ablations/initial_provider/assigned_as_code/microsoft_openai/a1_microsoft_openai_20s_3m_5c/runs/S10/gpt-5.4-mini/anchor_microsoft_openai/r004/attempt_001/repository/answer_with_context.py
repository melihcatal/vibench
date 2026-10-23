from model_client import get_client, get_model
from model_models import extract_text, wrap_text_result


def answer_with_context(payload, config=None):
    config = config or {}
    prompt = 'Use the context to answer the question faithfully.\n\nContext:\n' + payload['context'] + '\n\nQuestion:\n' + payload['question']
    with get_client(config) as client:
        response = client.chat.completions.create(model=get_model(config), messages=[{'role': 'user', 'content': prompt}])
    return wrap_text_result(extract_text(response))
