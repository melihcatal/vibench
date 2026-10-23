import json
import os

# Amazon Transcribe Streaming
# Service: Amazon Transcribe Streaming
# SDK: boto3
# Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY]):
    raise ValueError("AWS credentials not fully configured")

import boto3

client = boto3.client(
    "transcribe",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

def handle_transcribe_events(event_stream):
    """Process streaming events from Amazon Transcribe and yield partial/final transcripts."""
    for event in event_stream:
        # Decoded JSON payload from the WebSocket message
        payload = json.loads(event["Payload"])
        transcription_job = payload.get("TranscriptionJob")
        if not transcription_job:
            continue
        results = transcription_job.get("TranscriptionResult")
        if not results:
            continue
        items = results.get("Items", [])
        transcript_parts = []
        for item in items:
            # Partial interim results have a Timestamp but no alternative text
            alternative = item.get("Alternatives", [{}])[0]
            if alternative:
                transcript_parts.append(alternative.get("Transcript", ""))
        interim = " ".join(transcript_parts)
        final = payload.get("IsPartial", False) == False
        yield interim, final

if __name__ == "__main__":
    # Example usage with a mock event generator
    mock_events = [
        {"Payload": json.dumps({"TranscriptionJob": {"TranscriptionResult": {"Items": []}}})},
        {"Payload": json.dumps({"TranscriptionJob": {"TranscriptionResult": {"Items": [{"Alternatives": [{"Transcript": "Hello"}]}}]}})},
    ]
    for interim, is_final in handle_transcribe_events(mock_events):
        print(f"Interim: {interim}", end="\n" if is_final else "")
