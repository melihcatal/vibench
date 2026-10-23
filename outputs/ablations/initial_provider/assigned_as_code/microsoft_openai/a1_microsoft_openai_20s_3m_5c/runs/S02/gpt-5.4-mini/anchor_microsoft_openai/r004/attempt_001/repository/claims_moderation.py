from openai import OpenAI


def claims_moderation(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config['api_key'])
    response = client.moderations.create(
        model='omni-moderation-latest',
        input=payload.get('text', ''),
    )
    result = response.results[0]
    return {'flagged': result.flagged, 'categories': dict(result.categories)}
