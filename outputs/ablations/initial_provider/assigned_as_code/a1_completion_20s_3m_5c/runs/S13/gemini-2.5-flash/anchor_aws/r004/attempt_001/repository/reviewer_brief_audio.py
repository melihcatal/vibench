import boto3
from typing import Dict, Any
from safety_client import get_aws_client
from safety_models import AudioGenerationRequest, AudioGenerationResult

def reviewer_brief_audio(payload: AudioGenerationRequest, config: Dict[str, Any] = None) -> AudioGenerationResult:
    config = config or {}
    client = get_aws_client("polly", config)

    response = client.synthesize_speech(
        Text=payload.text_to_speak,
        OutputFormat=payload.output_format,
        VoiceId=payload.voice_id
    )

    audio_stream = response["AudioStream"].read()

    return AudioGenerationResult(audio_content=audio_stream)
