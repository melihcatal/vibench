import os
from openai import OpenAI

from model_client import get_client


def check_prompt_safety(payload, config=None):
    client = get_client(config)
    response = client.moderations.create(input=payload['text'])
    return {'flagged': response.results[0].flagged}