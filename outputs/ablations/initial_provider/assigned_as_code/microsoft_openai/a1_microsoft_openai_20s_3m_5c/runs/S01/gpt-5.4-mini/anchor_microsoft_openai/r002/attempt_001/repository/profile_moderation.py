import os

from openai import OpenAI

from identity_models import require_fields


def profile_moderation(payload, config=None):
    payload = require_fields(payload, ['text'])
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    result = client.moderations.create(model='omni-moderation-latest', input=payload['text'])
    flagged = result.results[0].flagged if result.results else False
    return {'flagged': flagged, 'categories': result.results[0].categories.model_dump() if result.results else {}}
