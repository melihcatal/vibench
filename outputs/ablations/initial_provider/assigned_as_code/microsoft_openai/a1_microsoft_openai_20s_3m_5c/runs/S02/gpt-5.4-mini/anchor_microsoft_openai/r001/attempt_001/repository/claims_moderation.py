from openai import OpenAI


def claims_moderation(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('openai_api_key'))
    response = client.moderations.create(
        model='omni-moderation-latest',
        input=payload.get('text', ''),
    )
    return {'flagged': response.results[0].flagged, 'categories': response.results[0].categories}
