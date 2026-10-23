from openai import OpenAI

from model_client import build_messages, get_client, get_model


def spoken_brief(payload, config=None):
    client = get_client(config)
    model = get_model(config)
    prompt = 'Rewrite the following model output as a concise spoken brief suitable for audio delivery.\n\nOutput:\n' + payload['text']
    response = client.chat.completions.create(model=model, messages=build_messages('', prompt))
    return {'brief': response.choices[0].message.content or ''}
