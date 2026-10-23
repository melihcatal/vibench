import os
from openai import OpenAI


def corpus_safety(payload, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key') or os.environ.get('OPENAI_API_KEY')) as client:
        moderation = client.moderations.create(model='omni-moderation-latest', input=payload['text'])
    return {'safe': not moderation.results[0].flagged}
