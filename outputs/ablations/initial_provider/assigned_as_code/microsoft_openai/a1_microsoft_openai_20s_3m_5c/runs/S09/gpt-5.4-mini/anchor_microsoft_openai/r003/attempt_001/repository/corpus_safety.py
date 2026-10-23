from openai import OpenAI


def corpus_safety(payload, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key')) as client:
        response = client.moderations.create(model='omni-moderation-latest', input=payload['text'])
    result = response.results[0]
    return {'flagged': result.flagged, 'categories': result.categories.model_dump()}
