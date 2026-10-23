import boto3

from speech_models import TranscriptChunk, normalize_text


def partial_results(events):
    boto3.client("transcribe", region_name="us-east-1")
    for event in events:
        text = normalize_text(getattr(event, "transcript", str(event)))
        if text:
            yield TranscriptChunk(text=text, is_final=bool(getattr(event, "is_final", False)))
