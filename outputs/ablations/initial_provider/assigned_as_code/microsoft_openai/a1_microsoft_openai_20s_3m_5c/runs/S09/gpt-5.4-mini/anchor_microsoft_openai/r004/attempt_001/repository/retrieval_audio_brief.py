import os
from openai import OpenAI


def retrieval_audio_brief(payload, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key') or os.environ.get('OPENAI_API_KEY')) as client:
        response = client.responses.create(model='gpt-4.1-mini', input=payload['results'])
    return {'brief': response.output_text}
