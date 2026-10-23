from openai import OpenAI
from model_client import get_config, get_model


def answer_with_context(payload, config=None):
    resolved = get_config(config)
    prompt = 'Use the provided context to answer the question. If the answer is not in the context, say you do not know.\n\nContext:\n' + payload['context'] + '\n\nQuestion:\n' + payload['question']
    with OpenAI(api_key=resolved['api_key']) as client:
        response = client.chat.completions.create(model=get_model(config), messages=[{'role': 'user', 'content': prompt}])
    return {'text': response.choices[0].message.content or ''}
