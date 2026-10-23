from openai import OpenAI

from document_models import extract_content, normalize_payload


def document_field_extraction(payload, config=None):
    payload = normalize_payload(payload)
    client = OpenAI(api_key=(config or {}).get('api_key'))
    response = client.responses.create(
        model='gpt-5.4-mini',
        input=[{'role': 'user', 'content': extract_content(payload)}],
    )
    return {'fields': getattr(response, 'output_text', '')}
