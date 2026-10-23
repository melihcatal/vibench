from openai import OpenAI


def corpus_safety(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('api_key'))
    response = client.moderations.create(model='omni-moderation-latest', input=payload['text'])
    return {'flagged': response.results[0].flagged}
