from openai import OpenAI


def reviewer_brief_audio(payload, config=None):
    client = OpenAI(api_key=(config or {}).get('api_key'))
    response = client.audio.speech.create(model='gpt-4o-mini-tts', voice=(config or {}).get('voice', 'alloy'), input=payload['text'])
    return {'audio': response}
