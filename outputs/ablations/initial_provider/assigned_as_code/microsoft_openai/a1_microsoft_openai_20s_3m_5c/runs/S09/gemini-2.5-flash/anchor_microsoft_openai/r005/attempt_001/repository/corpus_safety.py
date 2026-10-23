import os
from openai import OpenAI


def corpus_safety(payload, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY']) as client:
        moderation_response = client.moderations.create(input=payload['text'])
    
    results = moderation_response.results[0]
    
    if results.flagged:
        return {
            'is_safe': False,
            'categories': {category: value for category, value in results.categories.model_dump().items() if value},
            'category_scores': {category: value for category, value in results.category_scores.model_dump().items()}
        }
    else:
        return {'is_safe': True}