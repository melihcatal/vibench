import os
import assemblyai as aai
from speech_client import load_speech_config
from speech_models import normalize_segments


def diarized_transcript(audio_url: str):
    cfg = load_speech_config()
    aai.settings.api_key = cfg.api_key or os.environ["ASSEMBLYAI_API_KEY"]
    config = aai.TranscriptionConfig(speaker_labels=True)
    transcript = aai.Transcriber(config=config).transcribe(audio_url)
    payload = transcript.json_response
    return {"utterances": [s.__dict__ for s in normalize_segments(payload)]}
