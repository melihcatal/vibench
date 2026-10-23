from openai import OpenAI

from identity_client import load_identity_config


def profile_moderation(payload, config=None):
    config = load_identity_config(config)
    payload = payload or {}
    client = OpenAI(api_key=config.openai_api_key)
    response = client.moderations.create(model='omni-moderation-latest', input=payload.get('text', ''))
    result = response.results[0]
    return {'flagged': result.flagged, 'categories': result.categories.model_dump() if hasattr(result.categories, 'model_dump') else result.categories}
