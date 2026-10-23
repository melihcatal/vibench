import os
import assemblyai as aai

def transcribe_audio_assemblyai(audio_filepath: str) -> str:
    api_key = os.environ.get('ASSEMBLYAI_API_KEY')
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
    aai.settings.api_key = api_key
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_filepath)
    if transcript.status == aai.TranscriptStatus.completed:
        return transcript.text
    else:
        raise Exception(f"Transcription failed with status: {transcript.status}")
