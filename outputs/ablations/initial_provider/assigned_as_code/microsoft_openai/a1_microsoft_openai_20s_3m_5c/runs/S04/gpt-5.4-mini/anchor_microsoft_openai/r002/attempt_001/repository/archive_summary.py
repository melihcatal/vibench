import os
from openai import OpenAI
from speech_client import load_config


def archive_summary(payload, config=None):
    config = load_config(config)
    client = OpenAI(api_key=config['openai_api_key'] or os.environ['OPENAI_API_KEY'])
    response = client.responses.create(model=config['openai_model'], input=f"Summarize this transcript for archival storage:\n{payload.get('text', '')}")
    return {'summary': response.output_text}
