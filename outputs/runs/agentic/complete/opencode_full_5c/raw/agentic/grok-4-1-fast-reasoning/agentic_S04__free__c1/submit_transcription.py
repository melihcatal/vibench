import assemblyai as aai
from speech_client import get_client
from typing import Optional, Dict, Any


def submit_transcription(
    audio_file_path: str, config: Optional[Dict[str, Any]] = None
) -> str:
    client = get_client()
    audio_url = client.upload(audio_file_path)
    trans_config = {
        "language_code": "en",
        "punctuate": True,
        "format_text": True,
        "audio_url": audio_url,
    }
    if config:
        trans_config.update(config)
    transcript = client.transcripts.transcribe(trans_config)
    return transcript.id
