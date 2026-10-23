import assemblyai as aai
from speech_client import get_api_key
from speech_models import get_stt_config

def submit_transcription(audio_path: str) -> str:
    aai.settings.api_key = get_api_key()
    transcriber = aai.Transcriber()
    config_dict = get_stt_config(diarize=False)
    config = aai.TranscriptionConfig(**config_dict)
    transcript = transcriber.transcribe(audio_path, config=config)
    return transcript.id
