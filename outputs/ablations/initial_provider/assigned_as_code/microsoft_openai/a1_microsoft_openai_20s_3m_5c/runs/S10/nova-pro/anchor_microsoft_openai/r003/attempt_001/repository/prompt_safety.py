import os
from openai import OpenAI

def check_safety(payload, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY']) as client:
        response = client.moderations.create(input=payload['text'])
    return {'safety': response.results[0].flagged}
