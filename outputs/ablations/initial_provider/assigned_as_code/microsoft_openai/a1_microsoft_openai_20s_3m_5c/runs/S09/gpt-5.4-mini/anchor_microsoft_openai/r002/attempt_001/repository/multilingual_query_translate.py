from openai import OpenAI


def multilingual_query_translate(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('api_key'))
    response = client.responses.create(model='gpt-5.4-mini', input=payload['query'])
    return {'translated_query': response.output_text}
