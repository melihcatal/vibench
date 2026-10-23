import os

from openai import OpenAI

from speech_models import normalize_caption


def meeting_summary(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('api_key') or os.getenv('OPENAI_API_KEY'))
    transcript = '\n'.join(normalize_caption(chunk) for chunk in payload['chunks'])
    response = client.responses.create(model='gpt-4.1-mini', input=f'Summarize this meeting transcript concisely:\n{transcript}')
    return {'summary': response.output_text.strip()}
