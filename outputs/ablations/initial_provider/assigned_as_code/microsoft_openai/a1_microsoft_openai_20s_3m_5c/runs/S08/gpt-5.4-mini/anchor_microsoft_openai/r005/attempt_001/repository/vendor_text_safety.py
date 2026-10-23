import os
from openai import OpenAI


def vendor_text_safety(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('api_key') or os.environ.get('OPENAI_API_KEY'))
    text = payload.get('text') or ''
    response = client.moderations.create(model='omni-moderation-latest', input=text)
    result = response.results[0]
    return {'flagged': result.flagged, 'categories': result.categories, 'category_scores': result.category_scores}
