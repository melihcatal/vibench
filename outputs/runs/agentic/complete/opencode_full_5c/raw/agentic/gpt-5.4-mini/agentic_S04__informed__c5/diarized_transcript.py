import requests

from speech_client import get_config, headers, normalize_segments


def diarized_transcript(audio_url):
    cfg = get_config()
    payload = {"audio_url": audio_url, "speaker_labels": True}
    r = requests.post(
        f"{cfg['assemblyai_base_url']}/transcript",
        json=payload,
        headers=headers(),
        timeout=60,
    )
    r.raise_for_status()
    data = r.json()
    return {
        "id": data.get("id"),
        "status": data.get("status"),
        "segments": normalize_segments(data.get("utterances", [])),
    }
