from typing import List
import requests
import os
from speech_models import DiarizedTranscriptResponse, TranscriptSegment


def diarized_transcript(job_name: str) -> DiarizedTranscriptResponse:
    client = requests.Session()
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    url = "https://api.assemblyai.com/v2/transcript"

    headers = {"authorization": api_key, "content-type": "application/json"}

    # Submit job if not already submitted
    submit_payload = {
        "audio_url": f"s3://{os.getenv('AWS_TRANSCRIBE_OUTPUT_BUCKET')}/{job_name}.mp3",
        "speaker_labels": True,
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

    # Extract diarized segments
    utterances = response.json()["utterances"]
    segments: List[TranscriptSegment] = []
    for utterance in utterances:
        segments.append(
            TranscriptSegment(
                start_time=utterance["start"] / 1000,
                end_time=utterance["end"] / 1000,
                speaker_label=utterance["speaker"],
                text=utterance["text"],
            )
        )

    return DiarizedTranscriptResponse(segments=segments)
