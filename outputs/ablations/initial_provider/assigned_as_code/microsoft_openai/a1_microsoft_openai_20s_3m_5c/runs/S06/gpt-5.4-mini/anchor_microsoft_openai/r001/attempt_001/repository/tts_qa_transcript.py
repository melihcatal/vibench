from openai import OpenAI


def tts_qa_transcript(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('api_key'))
    response = client.audio.transcriptions.create(
        model='whisper-1',
        file=payload['audio_file'],
    )
    return {'text': response.text}
