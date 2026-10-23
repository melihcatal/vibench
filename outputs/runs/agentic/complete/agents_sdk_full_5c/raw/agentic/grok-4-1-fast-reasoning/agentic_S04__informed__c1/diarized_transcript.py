import assemblyai as aai
from speech_client import configure_assemblyai
from speech_models import base_config

def diarized_transcript(audio_file_path):
    configure_assemblyai()
    transcriber = aai.Transcriber()
    config = base_config(speaker_labels=True)
    transcript = transcriber.transcribe(audio_file_path, config)
    return transcript.id