import os
from openai import OpenAI

def transcribe_tts_audio(audio_path: str) -> str:
    """
    Transcribes synthesized QA audio samples using OpenAI Whisper to verify output.
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError('OPENAI_API_KEY environment variable not set')
    client = OpenAI(api_key=api_key)
    with open(audio_path, 'rb') as audio_file:
        transcript = client.audio.transcriptions.create(
            model='whisper-1',
            file=audio_file
        )
    return transcript.text
