import os

from openai import OpenAI

from speech_models import normalize_caption


def caption_embedding(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('api_key') or os.getenv('OPENAI_API_KEY'))
    texts = [normalize_caption(chunk) for chunk in payload['chunks']]
    response = client.embeddings.create(model='text-embedding-3-small', input=texts)
    return {'embeddings': [item.embedding for item in response.data], 'texts': texts}
