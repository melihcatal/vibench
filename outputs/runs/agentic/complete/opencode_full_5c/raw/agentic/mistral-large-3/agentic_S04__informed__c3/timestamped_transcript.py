from typing import List, Dict
import requests
import os
from speech_models import TimestampedTranscriptResponse, TranscriptSegment


def timestamped_transcript(job_name: str) -> TimestampedTranscriptResponse:
    client = requests.Session()
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    url = "https://api.assemblyai.com/v2/transcript"

    headers = {"authorization": api_key, "content-type": "application/json"}

    # Submit job if not already submitted
    submit_payload = {
        "audio_url": f"s3://{os.getenv('AWS_TRANSCRIBE_OUTPUT_BUCKET')}/{job_name}.mp3",
        "word_timestamps": True,
    }

    response = client.post(f"{url}", json=submit_payload, headers=headers)
    response.raise_for_status()
    transcript_id = response.json()["id"]

    # Poll for completion
    while True:
        response = client.get(f"{url}/{transcript_id}", headers=headers)
        response.raise_for_status()
        status = response.json()["status"]
        if status == "completed":
            break
        elif status == "failed":
            raise Exception("Transcription job failed")
        time.sleep(5)

    # Extract word timestamps and segments
    words = response.json()["words"]
    word_timestamps: List[Dict[str, float]] = []
    for word in words:
        word_timestamps.append(
            {
                "word": word["text"],
                "start": word["start"] / 1000,
                "end": word["end"] / 1000,
            }
        )

    segments: List[TranscriptSegment] = []
    for word in words:
        segments.append(
            TranscriptSegment(
                start_time=word["start"] / 1000,
                end_time=word["end"] / 1000,
                text=word["text"],
            )
        )

    return TimestampedTranscriptResponse(words=word_timestamps, segments=segments)
