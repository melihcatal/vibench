import os

from openai import OpenAI

from speech_models import normalize_caption_chunk


def live_caption_translate(payload, config=None):
    client = OpenAI(api_key=(config or {}).get('api_key') or os.getenv('OPENAI_API_KEY'))
    target_language = payload['target_language']
    source_text, is_final = normalize_caption_chunk(payload['caption'])
    response = client.responses.create(model='gpt-5.4-mini', input=f'Translate the following live caption into {target_language}: {source_text}')
    return {'text': response.output_text, 'is_final': is_final, 'target_language': target_language}
