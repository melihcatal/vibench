from openai import OpenAI


def claims_moderation(payload, config=None):
    client = OpenAI(api_key=config['api_key'])
    resp = client.moderations.create(model='omni-moderation-latest', input=payload['text'])
    return {'provider': 'openai', 'flagged': resp.results[0].flagged, 'categories': resp.results[0].categories.model_dump()}
