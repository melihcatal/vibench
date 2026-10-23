import requests

from speech_models import normalize_segments


def timestamped_transcript(payload, config=None):
    transcript_uri = payload["transcript_uri"]
    response = requests.get(transcript_uri, timeout=(config or {}).get("timeout", 30))
    response.raise_for_status()
    data = response.json()
    items = data.get("results", {}).get("items", [])
    segments = []
    for item in items:
        if "start_time" in item and "end_time" in item:
            segments.append(
                {
                    "start": float(item["start_time"]),
                    "end": float(item["end_time"]),
                    "text": item.get("alternatives", [{}])[0].get("content", ""),
                }
            )
    return {"segments": normalize_segments(segments), "raw": data}
