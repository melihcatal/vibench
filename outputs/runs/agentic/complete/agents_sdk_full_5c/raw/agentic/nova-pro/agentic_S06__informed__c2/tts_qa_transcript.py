import os
from assemblyai import Transcript

def transcribe_audio(audio_file):
    client = Transcript(os.environ.get('ASSEMBLYAI_API_KEY'))
    result = client.transcribe(audio_file)
    return result.text