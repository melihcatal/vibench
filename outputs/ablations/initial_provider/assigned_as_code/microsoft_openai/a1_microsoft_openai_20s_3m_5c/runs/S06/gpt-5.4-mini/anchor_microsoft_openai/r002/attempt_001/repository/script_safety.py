from openai import OpenAI


def script_safety(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('api_key'))
    response = client.moderations.create(model=config.get('model', 'omni-moderation-latest'), input=payload['text'])
    result = response.results[0]
    return {'safe': not result.flagged, 'categories': result.categories}
