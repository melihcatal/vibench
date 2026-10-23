import os
from openai import OpenAI

def get_client(config=None):
    config = config or {}
    api_key = config.get('api_key') or os.environ['OPENAI_API_KEY']
    return OpenAI(api_key=api_key)

def normalize_payload(payload):
    return {'text': payload['text']}

def parse_response(response):
    return {'embedding': response.data[0].embedding}