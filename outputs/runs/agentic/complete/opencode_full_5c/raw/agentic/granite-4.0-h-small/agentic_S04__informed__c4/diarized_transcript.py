import os
import json
from speech_client import SpeechClient


# Same-scenario: request speaker diarization for a recorded meeting
def diarized_transcript(audio_path, num_speakers=2):
    client = SpeechClient()
    # Build request with diarization enabled
    payload = client.create_diarized_request(audio_path, speaker_count=num_speakers)
    response = client.stt.submit_batch(payload)
    return response["job_id"]


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: diarized_transcript.py <audio_file.wav> [num_speakers]")
        sys.exit(1)
    audio_path = sys.argv[1]
    num_speakers = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    job_id = diarized_transcript(audio_path, num_speakers)
    print(f"Diarized transcription job submitted, ID: {job_id}")
