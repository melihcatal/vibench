# diarized_transcript.py
import os
import json
import boto3
from pathlib import Path
from speech_client import SpeechClient
from speech_models import SpeechModels

# Example: python diarized_transcript.py my_job_name output_bucket
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: diarized_transcript.py <job_name> <output_bucket>", file=sys.stderr)
        sys.exit(1)
    job_name = sys.argv[1]
    output_bucket = sys.argv[2]

    # AWS Transcribe supports speaker diarization via optional settings; here we request diarization with max 2 speakers
    client = SpeechClient.get_client()
    job_resp = client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': f's3://{output_bucket}/meeting_audio.wav'},
        LanguageCode='en-US',
        Settings={
            'DiarizationConfig': {
                'EnableDiarization': True,
                'MaxSpeakerCount': 2
            }
        }
    )
    print(json.dumps(job_resp, indent=2))
