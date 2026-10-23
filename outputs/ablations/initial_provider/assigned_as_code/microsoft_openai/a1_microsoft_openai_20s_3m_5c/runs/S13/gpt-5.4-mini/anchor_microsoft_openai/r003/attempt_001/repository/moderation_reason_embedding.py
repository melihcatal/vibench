from openai import OpenAI


def moderation_reason_embedding(payload, config=None):
    client = OpenAI(api_key=(config or {}).get('api_key'))
    text = payload.get('text', '') if isinstance(payload, dict) else str(payload)
    response = client.embeddings.create(model='text-embedding-3-small', input=text)
    return {'embedding': response.data[0].embedding}
