import openai


def secret_audit_embedding(payload, config=None):
    openai.api_key = config['openai_api_key']
    response = openai.Embedding.create(input=payload['audit_notes'], model="text-embedding-ada-002")
    return {"embedding": response['data'][0]['embedding']}