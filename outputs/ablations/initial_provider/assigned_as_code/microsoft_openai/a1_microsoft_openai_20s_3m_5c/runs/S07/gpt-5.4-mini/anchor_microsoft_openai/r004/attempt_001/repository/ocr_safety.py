from openai import OpenAI

from document_models import normalize_text


def ocr_safety(payload, config=None):
    payload = payload or {}
    config = config or {}
    text = normalize_text(payload.get('text'))
    client = OpenAI(api_key=config.get('api_key'))
    response = client.responses.create(model='gpt-4.1-mini', input='Assess the following document text for unsafe content and return concise JSON with fields safe and reason: ' + text)
    return {'analysis': response.output_text}
