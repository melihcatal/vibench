from embeddings_client import EmbeddingsClient
from embeddings_models import MODERATION_MODEL

def corpus_safety(payload, config=None):
    client = EmbeddingsClient(api_key=config.get('api_key') if config else None).get_client()

    text_to_check = payload['text']

    response = client.moderations.create(input=text_to_check)
    moderation_result = response.results[0]

    return {'flagged': moderation_result.flagged, 'categories': moderation_result.categories.model_dump()}
