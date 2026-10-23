from openai import OpenAI

from model_client import build_messages, get_client, get_model


def result_translate(payload, config=None):
    client = get_client(config)
    model = get_model(config)
    target_language = payload['target_language']
    text = payload['text']
    prompt = 'Translate the following text into ' + target_language + '.\n\nText:\n' + text
    response = client.chat.completions.create(model=model, messages=build_messages('', prompt))
    return {'text': response.choices[0].message.content or ''}
