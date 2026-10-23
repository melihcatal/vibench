from openai import OpenAI

from document_models import extract_content, normalize_payload


def ocr_embedding(payload, config=None):
    payload = normalize_payload(payload)
    config = config or {}
    client = OpenAI(api_key=config.get('api_key'))
    response = client.embeddings.create(model=config.get('model_id', 'text-embedding-3-small'), input=extract_content(payload))
    return {'embedding': response.data[0].embedding}
