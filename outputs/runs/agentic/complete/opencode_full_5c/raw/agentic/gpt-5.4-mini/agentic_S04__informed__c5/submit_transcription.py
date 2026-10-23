import requests

from speech_client import get_config, headers
from speech_models import TranscriptionRequest, normalize_transcript


def submit_transcription(audio_url, speaker_labels=False):
    cfg = get_config()
    payload = {"audio_url": audio_url, "speaker_labels": speaker_labels}
    r = requests.post(
        f"{cfg['assemblyai_base_url']}/transcript",
        json=payload,
        headers=headers(),
        timeout=60,
    )
    r.raise_for_status()
    return normalize_transcript(r.json())
