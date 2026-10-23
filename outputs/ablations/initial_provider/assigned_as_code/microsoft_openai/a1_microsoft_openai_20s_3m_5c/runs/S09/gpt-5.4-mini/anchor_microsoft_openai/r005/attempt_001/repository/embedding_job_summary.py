from openai import OpenAI

from embeddings_client import get_embeddings_model, get_openai_api_key


def embedding_job_summary(payload, config=None):
    config = config or {}
    with OpenAI(api_key=get_openai_api_key(config)) as client:
        response = client.embeddings.create(model=get_embeddings_model(config), input=payload['texts'])
    count = len(response.data)
    dimensions = len(response.data[0].embedding) if count else 0
    return {'job_count': count, 'embedding_dimensions': dimensions}
