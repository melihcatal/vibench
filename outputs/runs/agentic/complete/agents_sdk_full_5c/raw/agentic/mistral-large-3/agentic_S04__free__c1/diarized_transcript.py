import requests
from typing import List, Dict
from speech_models import DiarizedSegment

DIARIZATION_API_URL = "https://api.rev.ai/speechtotext/v1/jobs"
REV_AI_API_KEY = "rev_ai_api_key"  # Expected in environment

def diarized_transcript(audio_uri: str) -> List[DiarizedSegment]:
    """Requests speaker diarization for a recorded meeting using Rev AI."""
    headers = {"Authorization": f"Bearer {REV_AI_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "media_url": audio_uri,
        "metadata": "Meeting diarization",
        "diarization": {"enable": True, "speaker_channels_count": 2},
        "skip_diarization": False,
    }

    response = requests.post(DIARIZATION_API_URL, json=payload, headers=headers)
    response.raise_for_status()
    job_id = response.json()["id"]

    # Poll for diarization results (simplified)
    result_url = f"{DIARIZATION_API_URL}/{job_id}/transcript"
    result_response = requests.get(result_url, headers=headers)
    result_response.raise_for_status()
    transcript = result_response.json()

    segments = []
    for monologue in transcript.get("monologues", []):
        speaker = monologue["speaker"]["id"]
        for element in monologue["elements"]:
            if element["type"] == "text":
                segments.append(
                    DiarizedSegment(
                        speaker=speaker,
                        text=element["value"],
                        start_time=element["ts"],
                        end_time=element["end_ts"],
                    )
                )
    return segments