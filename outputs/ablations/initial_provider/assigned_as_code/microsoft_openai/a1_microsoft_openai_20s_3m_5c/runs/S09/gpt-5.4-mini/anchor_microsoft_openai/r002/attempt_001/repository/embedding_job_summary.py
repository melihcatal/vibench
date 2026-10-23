from openai import OpenAI


def embedding_job_summary(payload, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key')) as client:
        response = client.embeddings.create(model=config.get('model', 'text-embedding-3-small'), input=payload['texts'])
    return {'job_size': len(payload['texts']), 'embedded': len(response.data)}
