import os
from typing import Any, Dict

import boto3

from speech_models import TranscriptionRequest


def get_aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def get_bedrock_client():
    return boto3.client("bedrock-runtime", region_name=get_aws_region())


def get_transcribe_client():
    return boto3.client("transcribe", region_name=get_aws_region())


def build_transcription_settings(request: TranscriptionRequest) -> Dict[str, Any]:
    settings: Dict[str, Any] = {"ShowSpeakerLabels": request.speaker_labels}
    if request.timestamps:
        settings["ShowAlternatives"] = True
    return settings
