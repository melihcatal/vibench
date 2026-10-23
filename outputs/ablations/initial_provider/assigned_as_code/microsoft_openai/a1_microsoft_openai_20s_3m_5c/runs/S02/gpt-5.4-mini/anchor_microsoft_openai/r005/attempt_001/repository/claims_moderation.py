from openai import OpenAI


def claims_moderation(payload, config=None):
    payload = dict(payload or {})
    client = OpenAI(api_key=(config or {}).get('openai_api_key'))
    text = payload.get('text', '')
    response = client.moderations.create(model='omni-moderation-latest', input=text)
    return {'flagged': response.results[0].flagged, 'result': response.model_dump()}
