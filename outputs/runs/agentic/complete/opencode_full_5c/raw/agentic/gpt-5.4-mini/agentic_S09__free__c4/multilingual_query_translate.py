import os
from openai import OpenAI


def multilingual_query_translate(query, target_language='en'):
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    response = client.responses.create(model='gpt-4.1-mini', input=f'Translate to {target_language}: {query}')
    return response.output_text
