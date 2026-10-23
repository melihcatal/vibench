import os
from openai import OpenAI


def document_field_extraction(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY'])
    model = config.get('model', 'gpt-5.4-mini')
    response = client.responses.create(
        model=model,
        input=[{'role': 'user', 'content': payload['text']}],
    )
    return {'fields': response.output_text}
