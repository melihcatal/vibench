import os
import assemblyai as aai
from speech_client import load_speech_config


def submit_transcription(audio_url: str):
    cfg = load_speech_config()
    aai.settings.api_key = cfg.api_key or os.environ["ASSEMBLYAI_API_KEY"]
    transcript = aai.Transcriber().transcribe(audio_url)
    return {"id": transcript.id, "status": transcript.status}
