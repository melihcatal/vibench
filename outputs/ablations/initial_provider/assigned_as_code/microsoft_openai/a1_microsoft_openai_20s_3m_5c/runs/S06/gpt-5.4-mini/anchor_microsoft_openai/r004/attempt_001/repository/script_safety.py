from openai import OpenAI


def script_safety(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config['api_key'])
    response = client.moderations.create(model='omni-moderation-latest', input=payload['text'])
    result = response.results[0]
    return {'flagged': result.flagged, 'categories': result.categories.model_dump()}
