import os
from typing import Any, Dict, Optional

import boto3


def generate_spoken_briefing(
    platform_output: Any,
    voice_id: Optional[str] = None,
    engine: Optional[str] = None,
) -> Dict[str, Any]:
    text = platform_output if isinstance(platform_output, str) else str(platform_output)
    polly = boto3.client("polly")
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId=voice_id or os.environ.get("AWS_POLLY_VOICE_ID", "Joanna"),
        Engine=engine or os.environ.get("AWS_POLLY_ENGINE", "neural"),
    )
    return {
        "audio_stream": response["AudioStream"],
        "content_type": response.get("ContentType"),
        "request_characters": response.get("RequestCharacters"),
        "speech_marks": response.get("SpeechMarks"),
        "provider": "aws_polly",
    }
