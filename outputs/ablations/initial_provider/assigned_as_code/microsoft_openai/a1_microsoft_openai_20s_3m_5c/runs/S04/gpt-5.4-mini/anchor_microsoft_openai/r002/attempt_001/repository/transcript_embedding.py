import os
from openai import OpenAI
from speech_client import load_config


def transcript_embedding(payload, config=None):
    config = load_config(config)
    client = OpenAI(api_key=config['openai_api_key'] or os.environ['OPENAI_API_KEY'])
    response = client.embeddings.create(model=config['embedding_model'], input=payload.get('segments', []))
    return response.model_dump()
