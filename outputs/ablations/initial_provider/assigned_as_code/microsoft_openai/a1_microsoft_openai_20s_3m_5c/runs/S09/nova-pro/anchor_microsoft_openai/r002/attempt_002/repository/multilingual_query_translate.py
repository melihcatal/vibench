import os
from openai import OpenAI


def translate_query(query, target_language, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY']) as client:
        response = client.translations.create(model='text-davinci-003', text=query, target_language=target_language)
    return {'translated_query': response.text.strip()}