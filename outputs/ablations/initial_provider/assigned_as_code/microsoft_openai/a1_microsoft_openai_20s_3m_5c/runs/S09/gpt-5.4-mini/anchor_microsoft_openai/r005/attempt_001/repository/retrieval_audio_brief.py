from openai import OpenAI

from embeddings_client import get_openai_api_key


def retrieval_audio_brief(payload, config=None):
    config = config or {}
    with OpenAI(api_key=get_openai_api_key(config)) as client:
        response = client.audio.speech.create(
            model='gpt-4o-mini-tts',
            voice=payload.get('voice', 'alloy'),
            input=payload['summary'],
        )
    return {'audio_brief': response}
