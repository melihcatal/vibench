from openai import OpenAI

from embeddings_client import get_api_key, get_embedding_model


def embedding_job_summary(payload, config=None):
    config = config or {}
    with OpenAI(api_key=get_api_key(config)) as client:
        response = client.embeddings.create(model=get_embedding_model(config), input=payload['texts'])
    embeddings = [item.embedding for item in response.data]
    return {'count': len(embeddings), 'dimensions': len(embeddings[0]) if embeddings else 0, 'embeddings': embeddings}
