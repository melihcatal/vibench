import openai


def crypto_audit_embedding(notes, api_key=None):
    client = openai.OpenAI(api_key=api_key)
    response = client.embeddings.create(model='text-embedding-3-small', input=notes)
    return {'embedding': response.data[0].embedding, 'model': 'text-embedding-3-small', 'provider': 'OpenAI'}
