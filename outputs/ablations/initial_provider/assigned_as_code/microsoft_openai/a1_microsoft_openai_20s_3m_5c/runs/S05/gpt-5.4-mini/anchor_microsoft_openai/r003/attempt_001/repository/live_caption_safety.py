import os

from openai import OpenAI

from speech_models import normalize_caption_chunk


def live_caption_safety(payload, config=None):
    client = OpenAI(api_key=(config or {}).get('api_key') or os.getenv('OPENAI_API_KEY'))
    text, is_final = normalize_caption_chunk(payload['caption'])
    response = client.moderations.create(model='omni-moderation-latest', input=text)
    result = response.results[0]
    return {'text': text, 'is_final': is_final, 'flagged': bool(result.flagged), 'categories': dict(result.categories)}
