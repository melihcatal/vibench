import assemblyai as aai
from speech_client import get_client
from typing import Dict, Any, Optional


def submit_diarized_transcription(
    audio_file_path: str,
    speakers_expected: Optional[int] = None,
    config: Optional[Dict[str, Any]] = None,
) -> str:
    client = get_client()
    audio_url = client.upload(audio_file_path)
    trans_config = {
        "audio_url": audio_url,
        "speaker_labels": True,
        "language_code": "en",
        "punctuate": True,
        "format_text": True,
    }
    if speakers_expected:
        trans_config["speakers_expected"] = speakers_expected
    if config:
        trans_config.update(config)
    transcript = client.transcripts.transcribe(trans_config)
    return transcript.id
