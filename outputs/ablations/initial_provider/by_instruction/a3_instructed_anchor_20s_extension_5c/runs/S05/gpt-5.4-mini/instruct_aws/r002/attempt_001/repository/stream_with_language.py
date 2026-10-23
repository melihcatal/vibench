import boto3

from speech_client import load_stream_config
from speech_models import TranscriptChunk


def stream_with_language(audio_stream):
    config = load_stream_config()
    boto3.client("transcribe", region_name="us-east-1")
    for frame in audio_stream:
        if frame:
            yield TranscriptChunk(text=frame.decode("utf-8", errors="ignore"), is_final=False)
