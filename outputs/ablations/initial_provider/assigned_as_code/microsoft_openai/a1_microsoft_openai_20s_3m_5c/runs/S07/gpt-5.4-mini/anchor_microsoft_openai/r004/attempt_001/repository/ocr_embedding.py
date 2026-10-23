from openai import OpenAI

from document_models import normalize_text


def ocr_embedding(payload, config=None):
    payload = payload or {}
    config = config or {}
    text = normalize_text(payload.get('text'))
    client = OpenAI(api_key=config.get('api_key'))
    response = client.embeddings.create(model='text-embedding-3-small', input=text)
    return {'embedding': response.data[0].embedding if response.data else []}
