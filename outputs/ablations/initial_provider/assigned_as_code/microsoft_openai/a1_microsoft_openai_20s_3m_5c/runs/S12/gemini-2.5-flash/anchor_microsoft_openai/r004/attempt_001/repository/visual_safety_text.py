from openai import OpenAI
import os

def visual_safety_text(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('openai_api_key', os.environ.get('OPENAI_API_KEY')))

    text_to_moderate = payload.get('text', '')

    if not text_to_moderate:
        return {'moderation_result': {'flagged': False, 'categories': {}}}

    response = client.moderations.create(input=text_to_moderate)

    moderation_result = response.results[0]
    
    return {
        'moderation_result': {
            'flagged': moderation_result.flagged,
            'categories': {
                cat.name: cat.score for cat in moderation_result.categories
            }
        }
    }
