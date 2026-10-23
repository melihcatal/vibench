import os

from openai import OpenAI


def corpus_safety(payload, config=None):
    config = config or {}
    text = payload['text']
    with OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY']) as client:
        response = client.moderations.create(model='omni-moderation-latest', input=text)
    result = response.results[0]
    return {'flagged': result.flagged, 'categories': result.categories.model_dump(), 'category_scores': result.category_scores.model_dump()}
