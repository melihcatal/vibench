import requests

from speech_client import load_speech_config, speech_headers


def diarized_transcript(payload, config=None):
    cfg = load_speech_config(config)
    response = requests.post(
        f"https://{cfg.region}.api.cognitive.microsoft.com/speechtotext/transcriptions:submit",
        params={"api-version": "2024-11-15"},
        headers=speech_headers(cfg.api_key),
        json={
            "displayName": config.get("job_name", "diarized-meeting") if config else "diarized-meeting",
            "locale": payload["language_code"],
            "contentUrls": [payload["audio_uri"]],
            "properties": {"diarizationEnabled": True},
        },
        timeout=30,
    )
    response.raise_for_status()
    return {"job_id": response.json()["self"], "status": "SUBMITTED"}
