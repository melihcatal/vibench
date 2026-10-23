from openai import OpenAI


def message_safety(payload_text, config=None):
    client = OpenAI(api_key=(config or {}).get('api_key'))
    response = client.moderations.create(model='omni-moderation-latest', input=payload_text)
    result = response.results[0]
    return {'flagged': result.flagged, 'categories': result.categories.model_dump()}
