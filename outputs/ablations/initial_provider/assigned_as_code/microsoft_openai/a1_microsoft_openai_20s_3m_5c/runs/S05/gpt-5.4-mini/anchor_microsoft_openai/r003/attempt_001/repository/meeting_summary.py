import os

from openai import OpenAI


def meeting_summary(payload, config=None):
    client = OpenAI(api_key=(config or {}).get('api_key') or os.getenv('OPENAI_API_KEY'))
    transcript = '\n'.join(payload['transcript_chunks'])
    response = client.responses.create(model='gpt-5.4-mini', input=f'Summarize this meeting transcript concisely:\n{transcript}')
    return {'summary': response.output_text, 'language': payload.get('language_code')}
