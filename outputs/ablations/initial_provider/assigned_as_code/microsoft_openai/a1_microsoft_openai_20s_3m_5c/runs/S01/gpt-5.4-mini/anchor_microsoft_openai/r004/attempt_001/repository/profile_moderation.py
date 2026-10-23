from openai import OpenAI


def profile_moderation(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config['openai_api_key'])
    result = client.moderations.create(model='omni-moderation-latest', input=payload['text'])
    flagged = result.results[0].flagged
    return {'flagged': flagged, 'categories': result.results[0].categories.model_dump()}
