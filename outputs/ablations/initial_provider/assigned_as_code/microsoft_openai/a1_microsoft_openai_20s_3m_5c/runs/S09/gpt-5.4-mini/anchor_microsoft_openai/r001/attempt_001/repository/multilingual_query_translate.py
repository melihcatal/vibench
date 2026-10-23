import os

from openai import OpenAI


def multilingual_query_translate(payload, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY']) as client:
        response = client.responses.create(
            model='gpt-4.1-mini',
            input=[
                {'role': 'system', 'content': 'Translate the query into English only.'},
                {'role': 'user', 'content': payload['query']},
            ],
        )
    return {'translated_query': response.output_text}
