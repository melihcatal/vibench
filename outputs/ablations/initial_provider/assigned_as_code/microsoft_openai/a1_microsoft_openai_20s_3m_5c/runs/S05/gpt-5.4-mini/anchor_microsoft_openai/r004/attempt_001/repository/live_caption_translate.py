import os

from openai import OpenAI

from speech_models import normalize_caption


def live_caption_translate(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('api_key') or os.getenv('OPENAI_API_KEY'))
    target_language = payload['target_language']
    source_text = normalize_caption(payload['text'])
    response = client.responses.create(model='gpt-4o-mini', input=f'Translate the following caption into {target_language}: {source_text}')
    return {'text': response.output_text.strip(), 'target_language': target_language}
