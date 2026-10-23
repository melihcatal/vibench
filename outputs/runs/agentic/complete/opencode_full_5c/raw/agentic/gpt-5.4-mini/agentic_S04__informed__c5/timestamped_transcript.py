import requests

from speech_client import get_config, headers


def timestamped_transcript(transcript_id):
    cfg = get_config()
    r = requests.get(
        f"{cfg['assemblyai_base_url']}/transcript/{transcript_id}",
        headers=headers(),
        timeout=60,
    )
    r.raise_for_status()
    data = r.json()
    return {
        "id": data.get("id"),
        "status": data.get("status"),
        "words": data.get("words", []),
        "segments": data.get("utterances", []),
    }
