from openai import OpenAI

from embeddings_client import get_openai_api_key


def corpus_safety(payload, config=None):
    config = config or {}
    with OpenAI(api_key=get_openai_api_key(config)) as client:
        moderation = client.moderations.create(model='omni-moderation-latest', input=payload['text'])
    result = moderation.results[0]
    return {'safe': not result.flagged, 'categories': result.categories}
