from openai import OpenAI

from model_client import build_messages, get_client, get_model


def prompt_safety(payload, config=None):
    client = get_client(config)
    model = get_model(config)
    text = payload['text']
    response = client.chat.completions.create(
        model=model,
        messages=build_messages('Classify the content for safety concerns and return a brief verdict.', text),
    )
    return {'verdict': response.choices[0].message.content or ''}
