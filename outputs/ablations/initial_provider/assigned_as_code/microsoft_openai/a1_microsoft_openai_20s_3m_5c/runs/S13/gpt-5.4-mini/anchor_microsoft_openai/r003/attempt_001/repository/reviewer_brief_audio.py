from openai import OpenAI


def reviewer_brief_audio(payload, config=None):
    client = OpenAI(api_key=(config or {}).get('api_key'))
    text = payload.get('text', '') if isinstance(payload, dict) else str(payload)
    response = client.audio.speech.create(model='gpt-4o-mini-tts', voice='alloy', input=text)
    return {'audio': response.read()}
