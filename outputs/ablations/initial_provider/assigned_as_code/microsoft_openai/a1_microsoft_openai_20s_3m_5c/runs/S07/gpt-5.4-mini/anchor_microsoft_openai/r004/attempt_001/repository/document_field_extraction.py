from openai import OpenAI

from document_models import normalize_text


def document_field_extraction(payload, config=None):
    payload = payload or {}
    config = config or {}
    text = normalize_text(payload.get('text'))
    client = OpenAI(api_key=config.get('api_key'))
    response = client.responses.create(model='gpt-4.1-mini', input='Extract structured fields from the OCR-normalized document text as JSON: ' + text)
    return {'fields': response.output_text}
