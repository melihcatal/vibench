from openai import OpenAI


def script_translate(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('api_key'))
    model = config.get('model', 'gpt-4.1-mini')
    response = client.responses.create(model=model, input=payload['text'])
    return {'text': response.output_text}
