import requests

from speech_client import load_speech_config, speech_headers


def timestamped_transcript(job_id, config=None):
    cfg = load_speech_config(config)
    response = requests.get(
        f"https://{cfg.region}.api.cognitive.microsoft.com/speechtotext/transcriptions/{job_id}",
        params={"api-version": "2024-11-15", "$expand": "report"},
        headers=speech_headers(cfg.api_key),
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return {
        "job_id": data.get("self") or job_id,
        "timestamps": data.get("combinedRecognizedPhrases") or data.get("recognizedPhrases") or data.get("segments"),
    }
