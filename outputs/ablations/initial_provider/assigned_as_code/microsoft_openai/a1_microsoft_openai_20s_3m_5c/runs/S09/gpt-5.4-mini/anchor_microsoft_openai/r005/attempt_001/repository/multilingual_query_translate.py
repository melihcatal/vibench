from openai import OpenAI

from embeddings_client import get_openai_api_key


def multilingual_query_translate(payload, config=None):
    config = config or {}
    target_language = payload.get('target_language', 'en')
    with OpenAI(api_key=get_openai_api_key(config)) as client:
        response = client.responses.create(
            model='gpt-4o-mini',
            input=[
                {
                    'role': 'system',
                    'content': f'Translate the user query into {target_language} for multilingual search.',
                },
                {'role': 'user', 'content': payload['query']},
            ],
        )
    return {'translated_query': response.output_text}
