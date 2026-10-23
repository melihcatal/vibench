import os

from openai import OpenAI

from speech_models import normalize_caption


def live_caption_safety(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('api_key') or os.getenv('OPENAI_API_KEY'))
    text = normalize_caption(payload['text'])
    response = client.moderations.create(model='omni-moderation-latest', input=text)
    result = response.results[0]
    return {'text': text, 'flagged': result.flagged, 'categories': dict(result.categories)}
