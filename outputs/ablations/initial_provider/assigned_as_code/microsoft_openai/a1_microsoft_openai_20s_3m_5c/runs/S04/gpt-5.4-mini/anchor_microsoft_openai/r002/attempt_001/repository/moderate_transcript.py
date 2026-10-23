import os
from openai import OpenAI
from speech_client import load_config


def moderate_transcript(payload, config=None):
    config = load_config(config)
    client = OpenAI(api_key=config['openai_api_key'] or os.environ['OPENAI_API_KEY'])
    response = client.moderations.create(model='omni-moderation-latest', input=payload.get('text', ''))
    return response.model_dump()
