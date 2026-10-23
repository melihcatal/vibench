import assemblyai as aai
from speech_client import get_transcriber
from speech_models import get_base_config


def submit_transcription(audio_path: str, diarize: bool = False) -> str:
    transcriber = get_transcriber()
    config = get_base_config(diarize=diarize)
    transcript = transcriber.transcribe(audio_path, config=config)
    return str(transcript.id)
